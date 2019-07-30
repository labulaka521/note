# selector 分析
gomicro中的selector实现了一些基本的功能
- 负载均衡  
  随机选择(Random)  
  轮询的方式(RoundRobin)
- 缓存机制  
  通过缓存注册中心的服务来减缓每次调用来访问注册中心，交换注册中心的压力，每个缓存都有ttl查询服务现在缓冲中查找，如果没有就去注册中心查找，然后将查找的值缓存后返回潮汛的服务，并且通过watch及时的来更新缓存

## 创建Selector

这个主要初始化Selector，
```go
func NewSelector(opts ...Option) Selector {
	sopts := Options{
        // node选择算法默认是随机的
		Strategy: Random,
	}

	for _, opt := range opts {
		opt(&sopts)
	}
    // 注册中心
	if sopts.Registry == nil {
		sopts.Registry = registry.DefaultRegistry
	}

	s := &registrySelector{
		so: sopts,
    }
    // 初始化缓存
	s.rc = s.newCache()

	return s
}
```

`Select`是用来选择node的方法
```go
func (c *registrySelector) Select(service string, opts ...SelectOption) (Next, error) {
	sopts := SelectOptions{
		Strategy: c.so.Strategy,
	}

	for _, opt := range opts {
		opt(&sopts)
	}

	// 首先在cache中查找，如果没有查找到就在注册中心找到
	services, err := c.rc.GetService(service)
	if err != nil {
		return nil, err
	}

	// 过滤器，
	for _, filter := range sopts.Filters {
		services = filter(services)
	}

	// 服务为0，报错
	if len(services) == 0 {
		return nil, ErrNoneAvailable
	}
    // 选择一个node 
	return sopts.Strategy(services), nil
}
```