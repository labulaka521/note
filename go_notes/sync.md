# atomic

## atommic.Lood/Store
对XCHG和XADD这类X开头的指令，都会通过LOCK信号锁住内存总线，因此加不加LOCK前缀都是一样的。可以看到，由于硬件架构的支持，atomic.Load/Store和普通读写基本没有什么区别，这种CPU指令级别的锁非常快。因此通常我们将这类CPU指令级别的支持的Lock操作称为原子操作或无锁操作。
## atomic.Value
用于无锁存取任意值
```go
type Value struct {
	v interface{}
}
```

# Map
- 以空间换效率，通过read和dirty两个map来提高读取效率
- 优先从read map中读取(无锁)，否则再从dirty map中读取(加锁)
- 动态调整，当misses次数过多时，将dirty map提升为read map
- 延迟删除，删除只是为value打一个标记，在dirty map提升时才执行真正的删除

```go
type Map struct {
	// 当涉及dirty数据的操作 需要使用这个锁
	mu Mutex

	// 一个只读的数据结构，因为只读，所以不会有读写chong图
	// 所以从这个数据中读取总是安全的
	// 实际上，实际也会更新这个数据的entries，
	read atomic.Value // readOnly

	// dirty数据包含当前的entries，它包含最新的enteies，
	// 对于dirty的操作需要加锁，因为对它的操作可能会有读写竞争
	// 
	dirty map[interface{}]*entry

	// Load操作在read map中未找到，然后在dirty中读取，missed会自增，当misses与dirty的长度相等时，dirty被提升为read，并且重新分配dirty
	misses int
}
```
// readonly
```go
// readOnly 是一个不可变的结构，以原子方式存储在Map.read中
type readOnly struct {
	m       map[interface{}]*entry
	amended bool // 如果一些key不在read，但是在dirty中则为true
}
```

```go
type entry struct {
	// p 指向实际存储的接口值
	// p有三种状态
	// 如果 p == nil, 条目已经被删除，此时 m.dirty 等于 nil.
	//
	// 如果 p == expunged, 条目已经被删除, 此时m.dirty不等于nil,并且 m.dirty中不存在
	//
	// 是一个存在的值 存在read，如果m.dirty不等于nil 也存在与dirty中
	//
	// 被删除时，通过原子操作替换entry为nil，等到下一次dirty map创建时会替换nil为expungef 

	p unsafe.Pointer // *interface{}
}
// expunged是一个任意指针，用来标记已从dirty中删除的条目
var expunged = unsafe.Pointer(new(interface{}))
```
## Load
查找指定的key
```go
func (m *Map) Load(key interface{}) (value interface{}, ok bool) {
	// 先从无锁的read中读取
	read, _ := m.read.Load().(readOnly)
	e, ok := read.m[key]
	// 如果read不存在需要的key，但是amended为true表明dirty中有read不存在的key时，则开始尝试从dirty中读取
	if !ok && read.amended {
		m.mu.Lock()
		// 再次检测防止在加锁的时候dirty提升为read
		read, _ = m.read.Load().(readOnly)
		e, ok = read.m[key]
		if !ok && read.amended {
			e, ok = m.dirty[key]
			// 无论是否存在增加misses计数
			m.missLocked()
		}
		m.mu.Unlock()
	}
	if !ok {
		return nil, false
	}
	return e.load()
}

// 从entry中atomic.Loadpointer实际的接口值
func (e *entry) load() (value interface{}, ok bool) {
	p := atomic.LoadPointer(&e.p)
	if p == nil || p == expunged {
		return nil, false
	}
	return *(*interface{})(p), true
}

// 自增
func (m *Map) missLocked() {
	m.misses++
	// 如果misses小于dirty长度 返回
	if m.misses < len(m.dirty) {
		return
	}
	// 将dirty提升为read，然后dirty设置为nil misses设置为0
	m.read.Store(readOnly{m: m.dirty})
	m.dirty = nil
	m.misses = 0
}
```
## Store
存储一个键值
```go
func (m *Map) Store(key, value interface{}) {
	// 如果key存在于read中，则直接更改
	read, _ := m.read.Load().(readOnly)
	if e, ok := read.m[key]; ok && e.tryStore(&value) {
		return
	}

	m.mu.Lock()
	read, _ = m.read.Load().(readOnly)
	if e, ok := read.m[key]; ok {
		if e.unexpungeLocked() {
			// read中存在该key，但是p已经在dirty被删除了
			// 在dirty中存储该key

			m.dirty[key] = e
		}
		// read 中存在key 并且没有删除 则直接更新
		// read和dirty是共用entry的 所以直接更新内存地址的值就可以
		e.storeLocked(&value)
	} else if e, ok := m.dirty[key]; ok {
		// 如果read中不存在该key 且p!=expunged，但是在dirty中存在则直接更新该key，此时read还是没有该key
		e.storeLocked(&value)
	} else {
		if !read.amended { // m.dirty没有新的数据
			m.dirtyLocked() // dirty为nil的话从read中复制未删除的数据
			m.read.Store(readOnly{m: read.m, amended: true}) // 设置 amended 表示dirty存在read中不存在的值
		}
		// 将这个entry加入到m.dirty
		m.dirty[key] = newEntry(value)
	}
	m.mu.Unlock()
}

// 如果条目没有被标记删除，将key的值修改
// 如果条目被标记为expunged则返回false
func (e *entry) tryStore(i *interface{}) bool {
	p := atomic.LoadPointer(&e.p)
	if p == expunged {
		return false
	}
	for {
		if atomic.CompareAndSwapPointer(&e.p, p, unsafe.Pointer(i)) {
			return true
		}
		p = atomic.LoadPointer(&e.p)
		if p == expunged {
			return false
		}
	}
}

// 如果dirty为nil，把read中的未删除数据从read中复制过去
func (m *Map) dirtyLocked() {
	if m.dirty != nil {
		return
	}

	read, _ := m.read.Load().(readOnly)
	m.dirty = make(map[interface{}]*entry, len(read.m))
	for k, e := range read.m {
		// 将所有为nil的p修改为expunged
		// 拷贝所有不为expunged的值
		if !e.tryExpungeLocked() {
			m.dirty[k] = e
		}
	}
}

func (e *entry) tryExpungeLocked() (isExpunged bool) {
	p := atomic.LoadPointer(&e.p)
	for p == nil {
		// 如果p == nil 设置为punged后退出 不拷贝此数据
		if atomic.CompareAndSwapPointer(&e.p, nil, expunged) {
			return true
		}
		p = atomic.LoadPointer(&e.p)
	}
	return p == expunged
}
```

## Delete
删除

```go
func (m *Map) Delete(key interface{}) {
	read, _ := m.read.Load().(readOnly)
	e, ok := read.m[key]
	// 在read中查找
	if !ok && read.amended {
		// 不存在并且dirty存在read没有的key
		// 再次加锁检查
		m.mu.Lock()
		read, _ = m.read.Load().(readOnly)
		e, ok = read.m[key]
		// 直接从dirty中删除
		if !ok && read.amended {
			delete(m.dirty, key)
		}
		m.mu.Unlock()
	}
	if ok {
		e.delete()
	}
}

// 将key的值设置nil
func (e *entry) delete() (hadValue bool) {
	for {
		p := atomic.LoadPointer(&e.p)
		if p == nil || p == expunged {
			return false
		}
		if atomic.CompareAndSwapPointer(&e.p, p, nil) {
			return true
		}
	}
}
```


`sync.Map`还提供了`LoadOrStore/Range`操作,但没有提供`Len()`方法，如果需要统计有效值只能先提升dirty，再遍历read，`Range`方法已经做了

适合key值相对固定，读多写少的操作，因为新建key需要频繁提升dirty，

sync.map操作图解
![](../image/go-micro.svg)