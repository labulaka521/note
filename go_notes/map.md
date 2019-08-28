## 内部实现  
 映射是一种数据结构，用于存储一系列无序的键值对。  

 映射是一个集合，可以使用类似处理数组和切片的方式迭代映射中的元素。但映射是无序的集合，意味这没有办法预测键值对被返回的顺序。

无序的原因是映射实现使用了散列表
映射是一个存储键值对的无序集合。

映射的键可以是任何值。
可以使用`==`运算符做比较的值都可以作为映射的键  
切片，函数以及包含切片的结构类型这些类型具有引用语义，则不能作为映射的键  

映射在函数间传递并不会制造出该映射的一个副本。  
当传递映射给一个函数，并对这个映射做了修改时，所有对这个映射的引用都会察觉到这个修改  


### 小结  

- 数组是构造切片和映射的基石。
- Go 语言里切片经常用来处理数据的集合，映射用来处理具有键值对结构的数据。 
- 内置函数 make 可以创建切片和映射，并指定原始的长度和容量。也可以直接使用切片和映射字面量，或者使用字面量作为变量的初始值。 
- 切片有容量限制，不过可以使用内置的 append 函数扩展容量。 映射的增长没有容量或者任何限制。
- 内置函数 len 可以用来获取切片或者映射的长度。
- 内置函数 cap 只能用于切片。 
- 通过组合，可以创建多维数组和多维切片。也可以使用切片或者其他映射作为映射的值。但是切片不能用作映射的键。 
- 将切片或者映射传递给函数成本很小，并且不会复制底层的数据结构


### 哈希表和哈希函数
在记录的存储位置和它的关键字之间是建立一个确定的对应关系，使得每个关键字和一个存储位置能唯一对应。这个映射函数成为哈希函数，根据这个原则建立的表成为哈希表。

### 冲突
若两个key不相同 但是key所对应的存储位置相同，这种情况成为冲突

根据哈希函数f(key)和处理冲突的方法将一组关键字映射到一个有限的连续的地址集（区间）上，并以关键字在地址集中的“像”作为记录在表中的存储位置，这一映射过程称为构造哈希表。

go语言采用链表解决哈希冲突
`链表法`将一个bucket实现成一个链表，落在同一个bucket中的key都会插入这个链表  
`开放寻址法`则是碰撞发生后，通过一定的规律，在数组的后面挑选空位，用来防止新的key

## `map`内存模型    
```go
type hmap struct {
	// Note: the format of the hmap is also encoded in cmd/compile/internal/gc/reflect.go.
    // Make sure this stays in sync with the compiler's definition.
    // # map的大小
	count     int
    flags     uint8
    // buckets的对数
    B         uint8
    // 溢出桶的近似数目
    noverflow uint16 // approximate number of overflow buckets; see incrnoverflow for details
    // 哈希值
	hash0     uint32 
 
    // 指向bucket数组，大小为2^B 
    // 元素个数为0 就为nil bucket存储了key和value
    buckets    unsafe.Pointer 
    // 旧bucket 会是新bucket的一半
    oldbuckets unsafe.Pointer // previous bucket array of half the size, non-nil only when growing
    // 指示扩容进度 小于此地址的buckets迁移完成
	nevacuate  uintptr
    // 
	extra *mapextra // optional fields
}
```
buckets是一个指针，最终指向的bmap
```go
type bmap struct {
    tohhash [bucketCnt]uint8 // 一个bucket最多只可以存储8个
}
```

编译期间会动态的给bmap结构添加字段
```go
type bmap struct {
    topbits  [8]uint8
    keys     [8]keytype
    values   [8]valuetype
    pad      uintptr
    overflow uintptr
}
```
bmap就是桶，桶里面最多会装8个key，这些key因为经过哈希计算后，落在了同一个桶,然后根据计算出来的哈希值的高8位来确定key到底落入桶内的哪个位置 ,如果一个桶满了，那么就会重新构建bucket使用overflow指针连接起来
![](../image/hashbmap.png)

## 创建map
实际底层调用的是makemap函数
`/src/runtime/map.go`
```go
func makemap(t *maptype, hint int, h *hmap) *hmap {
	if hint < 0 || hint > int(maxSliceCap(t.bucket.size)) {
		hint = 0
	}

	// 初始化hmap
	if h == nil {
		h = new(hmap)
	}
	h.hash0 = fastrand()

	// 确定B的大小
	B := uint8(0)
	for overLoadFactor(hint, B) {
		B++
	}
	h.B = B

	// 初始化Hash TABLE
	// if B == 0, the buckets field is 延迟分配 (in 赋值)
    // If hint is large zeroing this memory could take a while.
    // 如果长度比较大，分配内存会花费长一点时间
	if h.B != 0 {
		var nextOverflow *bmap
		h.buckets, nextOverflow = makeBucketArray(t, h.B, nil)
		if nextOverflow != nil {
			h.extra = new(mapextra)
			h.extra.nextOverflow = nextOverflow
		}
	}

	return h
}
```

## key定位过程
key经过哈希计算得到哈希值，计算它到底要落在哪个桶，只会用到最后B个bit位，桶的数量是`2^B`
使用哈希值的后B个bit位，然后就是落在这个桶中的。  再用哈希位的高8位，找到此此key在bucket中的位置

当两个不同的key落在同一个桶中，也就是发生了哈希冲突，也就是发送了哈希冲突，冲突的解决方案是使用链表法，在bucket中，从前往后找到第一个空位放入，查找某个key时，先找到对应的桶，再去遍历bucket中的ekey

低B位寻找对应的桶bucket，使用高8位在桶中找到对应的tophash值，如果没有找到，而且overflow不为空，还要去overflow bucket中找。
```go
func mapaccess1(t *maptype, h *hmap, key unsafe.Pointer) unsafe.Pointer {
	if raceenabled && h != nil {
		callerpc := getcallerpc()
		pc := funcPC(mapaccess1)
		racereadpc(unsafe.Pointer(h), callerpc, pc)
		raceReadObjectPC(t.key, key, callerpc, pc)
	}
	if msanenabled && h != nil {
		msanread(key, t.key.size)
    }
    // h 为nil 或者总数为0 直接返回
	if h == nil || h.count == 0 {
		return unsafe.Pointer(&zeroVal[0])
    }
    // 写和读冲突
	if h.flags&hashWriting != 0 {
		throw("concurrent map read and map write")
    }
    // hash算法
    alg := t.key.alg
    // 计算哈希值
    hash := alg.hash(key, uintptr(h.hash0))
    // 2^B
    m := bucketMask(h.B)
    // bucket的地址
    b := (*bmap)(add(h.buckets, (hash&m)*uintptr(t.bucketsize)))
    // 是否发送扩容
	if c := h.oldbuckets; c != nil {
		if !h.sameSizeGrow() {
			// There used to be half as many buckets; mask down one more power of two.
			m >>= 1
		}
		oldb := (*bmap)(add(c, (hash&m)*uintptr(t.bucketsize)))
		if !evacuated(oldb) {
			b = oldb
		}
    }
    // 计算高8为的hash
    top := tophash(hash)
    // 获取bucket 在第一个没找到会去overflow链接的下一个bucket中去找
	for ; b != nil; b = b.overflow(t) {
        // 遍历8个bucket
		for i := uintptr(0); i < bucketCnt; i++ {
			if b.tophash[i] != top {
                // 不匹配继续
				continue
            }
            // key是指针
			k := add(unsafe.Pointer(b), dataOffset+i*uintptr(t.keysize))
			if t.indirectkey {
				k = *((*unsafe.Pointer)(k))
            }
            // 定位value位置
			if alg.equal(key, k) {
				v := add(unsafe.Pointer(b), dataOffset+bucketCnt*uintptr(t.keysize)+i*uintptr(t.valuesize))
				if t.indirectvalue {
					v = *((*unsafe.Pointer)(v))
				}
				return v
			}
		}
    }
    // 返回零值
	return unsafe.Pointer(&zeroVal[0])
}
```
#### 两种get操作
Go 语言中读取 map 有两种语法：带 comma 和 不带 comma,编译器分析代码后将两种不同的语法对应到底层两个不同的函数
```go
// src/runtime/hashmap.go
func mapaccess1(t *maptype, h *hmap, key unsafe.Pointer) unsafe.Pointer
func mapaccess2(t *maptype, h *hmap, key unsafe.Pointer) (unsafe.Pointer, bool)
```


#### map为什么是无序的
```go
func mapiterinit(t *maptype, h *hmap, it *hiter) {
	// ...
	it.t = t
	it.h = h

	// grab snapshot of bucket state
	it.B = h.B
	it.buckets = h.buckets
	if t.bucket.kind&kindNoPointers != 0 {
		// Allocate the current slice and remember pointers to both current and old.
		// This preserves all relevant overflow buckets alive even if
		// the table grows and/or overflow buckets are added to the table
		// while we are iterating.
		h.createOverflow()
		it.overflow = h.extra.overflow
		it.oldoverflow = h.extra.oldoverflow
	}

	// 使用一个随机数来决定从哪个桶开始遍历
	r := uintptr(fastrand())
	if h.B > 31-bucketCntBits {
		r += uintptr(fastrand()) << 31
	}
	it.startBucket = r & bucketMask(h.B)
	it.offset = uint8(r >> h.B & (bucketCnt - 1))

	// iterator state
	it.bucket = it.startBucket

	// Remember we have an iterator.
	// Can run concurrently with another mapiterinit().
	if old := h.flags; old&(iterator|oldIterator) != iterator|oldIterator {
		atomic.Or8(&h.flags, iterator|oldIterator)
	}

	mapiternext(it)
}

```