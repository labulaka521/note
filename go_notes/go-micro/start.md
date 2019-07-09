# micro.Newservice
```go
service := micro.NewService(
	micro.Name("srv_name"),
	micro.Version("latest"),
	micro.RegisterTTL(time.Second*30),
	micro.RegisterInterval(time.Second*15),
	micro.Registry(registry.Etcd(cfg.EtcdConfig.Endpoints...)),
	)
```
`micro.NewService`创建服务，实际是返回一个实现`micro.Service`接口的struct `service`
```go
type service struct {
	opts Options

	once sync.Once
}
```
`NewService`实际调用的是`newService`这个函数
```go
func newService(opts ...Option) Service {
	options := newOptions(opts...)

	options.Client = &clientWrapper{
		options.Client,
		metadata.Metadata{
			HeaderPrefix + "From-Service": options.Server.Options().Name,
		},
	}

	return &service{
		opts: options,
	}
}
```

然后`newOptions`将传入的参数初始化 返回`micro.Options`这个结构体,然后将返回初始化好的配置置入`micro.service`中然后再返回，这时创建新服务已经完成。


micro实现了可以默认配置参数的一种方法

创建服务中传入的配置全是返回这种格式的配置
```go
type Option func(*Options)
```

**以在创建服务时指定服务名称为例**
`micro.Name("crocodile.srv.actuator")`会返回一个`Option`的函数
然后进入`Name`中查看实际返回的是
```go
// Name of the service
func Name(n string) Option {
	return func(o *Options) {
		o.Server.Init(server.Name(n))
	}
}
```
这种函数的格式刚好符合`micro.Option`的格式，并且返回的函数需要传入一个`Options`的结构体,
参数n就是传入的服务名称，然后进入`service.Name`函数，
```
func Name(n string) Option {
	return func(o *Options) {
		o.Name = n
	}
}
```
在此函数Name又返回一个`micro.Option`的的函数，在这个函数`o.Name = n`可以看到将`service.Options.Name`修改为了传入的服务名称

最后是通过`options := newOptions(opts...)`这句才将所有的参数初始化完成的
```go
func newOptions(opts ...Option) Options {
	opt := Options{
		Broker:    broker.DefaultBroker,
		Cmd:       cmd.DefaultCmd,
		Client:    client.DefaultClient,
		Server:    server.DefaultServer,
		Registry:  registry.DefaultRegistry,
		Transport: transport.DefaultTransport,
		Context:   context.Background(),
	}

	for _, o := range opts {
		o(&opt)
	}

	return opt
}
```
`opt`是一个Options结构体，并且全部都有默认值，`o`为修改配置的函数，上面看到所有修改配置都是一个可以传入`Options指针`参数的函数，在这个函数内将`Options`的值才修改完成的，所有这个循环结束后，配置的参数也就生效了，在micro中随处可以很多这样修改配置的函数，既可以默认参数，又可以修改默认的参数，很方便

然后返回修改后的结构体返回，然后下面就到了
然后构造service



在传入的`Option`顺序这里有一个`小小的坑`  
在NewService传入的参数中，需要注意一点，看`micro.Registry`这个配置注册中心的函数
```go
// Registry sets the registry for the service
// and the underlying components
func Registry(r registry.Registry) Option {
	return func(o *Options) {
		o.Registry = r
		// Update Client and Server
		o.Client.Init(client.Registry(r))
		o.Server.Init(server.Registry(r))
		// Update Selector
		o.Client.Options().Selector.Init(selector.Registry(r))
		// Update Broker
		o.Broker.Init(broker.Registry(r))
	}
}
```
这个里面初始化了`Client` `Service` `Selector` `Broker`的注册中心，但是如果我们需要自定义这些的时候就会出现问题，比如自定义`broker`的地址，
```go
micro.Broker(
	broker.NewBroker(
		broker.Addrs(cfg.ExecuteConfig.Address),
		broker.Registry(registry.Etcd(cfg.EtcdConfig.Endpoints...)),
	),
),
```
在创建`broker`的时候如果这个`Option`是在`micro.Registry`后面时，如果我们想用非默认的注册中心，就必须填写`broker`的注册中心否将会使用默认的注册中心`mdns`，这是因为`NewBroker`
```go
func NewBroker(opts ...Option) Broker {
	return newHttpBroker(opts...)
}
```
```go
func newHttpBroker(opts ...Option) Broker {
	options := Options{
		Codec:   json.Marshaler{},
		Context: context.TODO(),
	}

	for _, o := range opts {
		o(&options)
	}

	// set address
	addr := ":0"
	if len(options.Addrs) > 0 && len(options.Addrs[0]) > 0 {
		addr = options.Addrs[0]
	}

	// get registry
	reg, ok := options.Context.Value(registryKey).(registry.Registry)
	if !ok {
		reg = registry.DefaultRegistry
	}
```
创建了一个新的`broker`并且覆盖了在`micro.Registry`对`broker`的配置，可以看到如果不传入一个注册中心的地址,就会使用默认的`registry.DefaultRegistry`的注册中心  
但是如果我们将这句代码放在`micro.Registry`的上方，就不需要指定指定注册中心的地址，这个就会先于`micro.Registry`中对`broker`的配置运行，而先返回一个将地址修改的`Broker`配置，然后`micro.Registry`再次修改`broker`的注册中心。


# srv.Init
它的工作主要是再次渲染传入Init的Option配置项，然后再初始化命令行参数。

```go
func (s *service) Init(opts ...Option) {
    // process options
    // 生效传入的配置
	for _, o := range opts {
		o(&s.opts)
	}
    // 生效命令行传入的配置
	s.once.Do(func() {
		// Initialise the command flags, overriding new service
		_ = s.opts.Cmd.Init(
			cmd.Broker(&s.opts.Broker),
			cmd.Registry(&s.opts.Registry),
			cmd.Transport(&s.opts.Transport),
			cmd.Client(&s.opts.Client),
			cmd.Server(&s.opts.Server),
		)
	})
}
```
所以在micro中配置生效的的顺序为  
`随构造函数传入的参数` < `Init函数传入的函数` < `Cmd传入的参数`

# registry
将实现proto定义的接口的handler注册到server中

# run

`srv.Run`的代码
```
func (s *service) Run() error {
	if err := s.Start(); err != nil {
		return err
	}

	ch := make(chan os.Signal, 1)
	signal.Notify(ch, syscall.SIGTERM, syscall.SIGINT, syscall.SIGQUIT)

	select {
	// wait on kill signal
	case <-ch:
	// wait on context cancel
	case <-s.opts.Context.Done():
	}

	return s.Stop()
}
```
`Run`实际是调用`Start`这个方法然后会监听系统的信号，接收到这些中断信号时，然后会运行`s.Stop`这个方法来关闭一系列服务
`Start`和`Stop`这两个方法都可以设置在这两个方法启动前后运行的方法，来达到自定义一些功能的方法
在初始化配置的时候可以从`micro.BeforeStart micro.BeforeStop`配置，然后将这些方法放在`micro.Options`中的`Brfore...` `After...`等切片中
```go
type Options struct {
	Broker    broker.Broker
	Cmd       cmd.Cmd
	Client    client.Client
	Server    server.Server
	Registry  registry.Registry
	Transport transport.Transport

	// Before and After funcs
	BeforeStart []func() error
	BeforeStop  []func() error
	AfterStart  []func() error
	AfterStop   []func() error

	// Other options for implementations of the interface
	// can be stored in a context
	Context context.Context
}
```
然后到启动server的地方
```go
func (s *service) Start() error {
	for _, fn := range s.opts.BeforeStart {
		if err := fn(); err != nil {
			return err
		}
	}

	if err := s.opts.Server.Start(); err != nil {
		return err
	}

	for _, fn := range s.opts.AfterStart {
		if err := fn(); err != nil {
			return err
		}
	}

	return nil
}
```
然后进入`s.opts.Server.Start`方法中去
```go
func (s *rpcServer) Start() error {
	registerDebugHandler(s)
	config := s.Options()

	// transport的传输
	ts, err := config.Transport.Listen(config.Address)
	if err != nil {
		return err
	}

	log.Logf("Transport [%s] Listening on %s", config.Transport.String(), ts.Addr())

	// swap address
	s.Lock()
	addr := s.opts.Address
	s.opts.Address = ts.Addr()
	s.Unlock()

	// broker链接
	if err := config.Broker.Connect(); err != nil {
		return err
	}

	log.Logf("Broker [%s] Connected to %s", config.Broker.String(), config.Broker.Address())

	// 注册服务
	if err = s.opts.RegisterCheck(s.opts.Context); err != nil {
		log.Logf("Server %s-%s register check error: %s", config.Name, config.Id, err)
	} else {
		// announce self to the world
		if err = s.Register(); err != nil {
			log.Log("Server %s-%s register error: %s", config.Name, config.Id, err)
		}
	}

	exit := make(chan bool)

	go func() {
		for {
			// listen for connections
			err := ts.Accept(s.ServeConn)

			// TODO: listen for messages
			// msg := broker.Exchange(service).Consume()

			select {
			// check if we're supposed to exit
			case <-exit:
				return
			// check the error and backoff
			default:
				if err != nil {
					log.Logf("Accept error: %v", err)
					time.Sleep(time.Second)
					continue
				}
			}

			// no error just exit
			return
		}
	}()

	go func() {
		t := new(time.Ticker)

		// only process if it exists
		if s.opts.RegisterInterval > time.Duration(0) {
			// new ticker
			t = time.NewTicker(s.opts.RegisterInterval)
		}

		// return error chan
		var ch chan error

	Loop:
		for {
			select {
			// register self on interval
			case <-t.C:
				s.RLock()
				registered := s.registered
				s.RUnlock()
				if err = s.opts.RegisterCheck(s.opts.Context); err != nil && registered {
					log.Logf("Server %s-%s register check error: %s, deregister it", config.Name, config.Id, err)
					// deregister self in case of error
					if err := s.Deregister(); err != nil {
						log.Logf("Server %s-%s deregister error: %s", config.Name, config.Id, err)
					}
				} else {
					if err := s.Register(); err != nil {
						log.Logf("Server %s-%s register error: %s", config.Name, config.Id, err)
					}
				}
			// wait for exit
			case ch = <-s.exit:
				t.Stop()
				close(exit)
				break Loop
			}
		}

		// deregister self
		if err := s.Deregister(); err != nil {
			log.Logf("Server %s-%s deregister error: %s", config.Name, config.Id, err)
		}

		// wait for requests to finish
		if s.wg != nil {
			s.wg.Wait()
		}

		// close transport listener
		ch <- ts.Close()

		// disconnect the broker
		config.Broker.Disconnect()

		// swap back address
		s.Lock()
		s.opts.Address = addr
		s.Unlock()
	}()

	return nil
}
```

从上往下看依次启动`transport`监听端口 -> `broker`的监听端口 -> registry注册 -> 接收链接请求 -> 持续注册
> 这里的端口如果没有默认的话都是随机的端口
```go
// use RegisterCheck func before register
if err = s.opts.RegisterCheck(s.opts.Context); err != nil {
	log.Logf("Server %s-%s register check error: %s", config.Name, config.Id, err)
} else {
	// announce self to the world
	if err = s.Register(); err != nil {
		log.Log("Server %s-%s register error: %s", config.Name, config.Id, err)
	}
}
```
`s.opts.RegistryCheck`是在注册前的检查函数，默认为  
`DefaultRegisterCheck        = func(context.Context) error { return nil }`  
检查无误后然后开始真正注册服务到注册中心`s.Register()`
>由于go-micro可插拔的特性，注册中心只要实现`registry.Registry`这个接口，就可以作为一个插件 。  

`s.Registry`将自已的信息全部注册到了注册中心，这里面有注册的服务和订阅消息的注册

然后`transport.Accept`监听链接，再往下走又是一个go关键字，这个函数是设置服务注册间隔和注册信息的有效性的，以便服务下线后可以自动从注册中心清除,在服务初始化的时候可以通过
```go
// 注册信息的有效时长
micro.RegisterTTL(time.Second*30),
// 每隔多久注册一次
micro.RegisterInterval(time.Second*15),
```
来设置

