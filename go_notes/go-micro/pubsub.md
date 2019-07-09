# go micro 中的发布订阅(HTTP)

## 初始化订阅消息
订阅的代码
```go
executor := &subscriber.Executor{}

//Register Struct as Subscriber
err = micro.RegisterSubscriber("topic.srv.name", service.Server(), executor, server.SubscriberQueue("test"))
```
订阅消息时可以设置消息队列，如果不设置消息就会发不到所有的节点上，如果设置了就会随机选择一个节点发送消息
```go
type Executor struct {}
func (e *Executor) ExecEvent(ctx context.Context, exMsg *pbexecutor.ExecuteMsg) (err error) {
    fmt.Println(exMsg)
}
```

注册订阅的时候可以传入一个`struct` 或者 `func`
`struct`需要实现处理消息的方法，

进入函数`RegisterSubscriber`
```go
// RegisterSubscriber是用于注册订阅者的语法糖
func RegisterSubscriber(topic string, s server.Server, h interface{}, opts ...server.SubscriberOption) error {
	return s.Subscribe(s.NewSubscriber(topic, h, opts...))
}
```
首先看`s.NewSubscriber`，这个方法返回的是一个Subscriber的接口,这个接口有四个方法
```go
// Subscriber interface represents a subscription to a given topic using
// a specific subscriber function or object with endpoints.
type Subscriber interface {
    // 订阅的名称
    Topic() string
    // 处理订阅消息的函数
    Subscriber() interface{}
    // 订阅信息注册的信息
    Endpoints() []*registry.Endpoint
    // 配置
	Options() SubscriberOptions
}
```
然后先进入`s.NewSubscriber`这个方法
>github.com/micro/go-micro/server/rpc_server.go:230
```go
func (s *rpcServer) NewSubscriber(topic string, sb interface{}, opts ...SubscriberOption) Subscriber {
	return newSubscriber(topic, sb, opts...)
}
```
实际调用的是`newSubscriber`这个函数来来进行新建subsciber
```go
func newSubscriber(topic string, sub interface{}, opts ...SubscriberOption) Subscriber {
	options := SubscriberOptions{
		AutoAck: true,
	}

	for _, o := range opts {
		o(&options)
	}

	var endpoints []*registry.Endpoint
	var handlers []*handler
    // 在注册的时候可以传入一个函数或者一个结构体
	// 然后在这里利用reflectl来获取所有的注册的处理消息的事件
	// 如果是一个函数
	if typ := reflect.TypeOf(sub); typ.Kind() == reflect.Func {
		h := &handler{
			method: reflect.ValueOf(sub),
		}

		switch typ.NumIn() {
		case 1:
			h.reqType = typ.In(0)
		case 2:
			h.ctxType = typ.In(0)
			h.reqType = typ.In(1)
		}

		handlers = append(handlers, h)

		endpoints = append(endpoints, &registry.Endpoint{
			Name:    "Func",
			Request: extractSubValue(typ),
			Metadata: map[string]string{
				"topic":      topic,
				"subscriber": "true",
			},
		})
	} else {
		// 否则就是一个结构体 然后解析后这个结构体的所有方法
		hdlr := reflect.ValueOf(sub)
		name := reflect.Indirect(hdlr).Type().Name()

		for m := 0; m < typ.NumMethod(); m++ {
            method := typ.Method(m)
            // 方法自已
			h := &handler{
				method: method.Func,
			}
            // 方法的参数 默认只提取方法的前两个参数
            // 
			switch method.Type.NumIn() {
			case 2:
				h.reqType = method.Type.In(1)
			case 3:
				h.ctxType = method.Type.In(1)
				h.reqType = method.Type.In(2)
			}
            
			handlers = append(handlers, h)
            // 构建注册topic的信息
			endpoints = append(endpoints, &registry.Endpoint{
				Name:    name + "." + method.Name,
				Request: extractSubValue(method.Type),
				Metadata: map[string]string{
					"topic":      topic,
					"subscriber": "true",
				},
			})
		}
	}

	return &subscriber{
       
        rcvr:       reflect.ValueOf(sub),
       
        typ:        reflect.TypeOf(sub),
        // 订阅的名称
        topic:      topic,
        // 传入的订阅参数
        subscriber: sub,
        // 处理消息事件的函数
        handlers:   handlers,
        // 订阅信息的注册信息
        endpoints:  endpoints,
        // 定语的配置
		opts:       options,
	}
}
```
`newSubscriber`主要接收两个参数`topic` `sub`
`topic`是这个订阅的名称，`sub`是接收订阅消息处理模块,`sub`可以是一个`struct`或者一个`func`
如果传入的参数类型是函数，利用反射获取到这个函数的参数，函数的参数有两种`(ctx,par)``(par)`
利用反射获取到这个函数的参数的类型，然后再构建这个topic的注册信息
```go
endpoints = append(endpoints, &registry.Endpoint{
			Name:    "Func",
			Request: extractSubValue(typ),
			Metadata: map[string]string{
				"topic":      topic,
				"subscriber": "true",
			},
		})
```
如果传入的是一个结构体，那么这个结构体就必须实现来处理消息事件的方法，然后这里利用反射的方法获取这个struct的所有方法，名称等信息
使用`subscriber`结构体包装后返回，这里实现了`Subscriber`这个接口
然后返回的值会当作`s.Subscribe`的参数传入，检查正确后就会存储在`rpcServer.subscribers`这个字段中，至此订阅信息已经初始化完成，下来就是就是注册到注册中心了
```go
func (s *rpcServer) Subscribe(sb Subscriber) error {
    // 类型转换 判断传入的订阅信息是否争取
	sub, ok := sb.(*subscriber)
	if !ok {
		return fmt.Errorf("invalid subscriber: expected *subscriber")
    }
    // 处理的函数如果为0就报错退出
	if len(sub.handlers) == 0 {
		return fmt.Errorf("invalid subscriber: no handler functions")
	}

	if err := validateSubscriber(sb); err != nil {
		return err
	}

	s.Lock()
    defer s.Unlock()
    // 保存订阅的信息
	_, ok = s.subscribers[sub]
	if ok {
		return fmt.Errorf("subscriber %v already exists", s)
	}
	s.subscribers[sub] = nil
	return nil
}
```

## 注册订阅信息
上面就是订阅服务初始化的步骤了，初始化后会讲subuscriber的信息存储在创建的server中，然后就到将这些信息启动注册到注册中心了
在[启动过程](./start.md)中我们介绍了程序的启动过程,事件广播/订阅主要由`broker`接口来完成

```go
func (s *rpcServer) Start() error {
    // 省略
	// 连接broker
	if err := config.Broker.Connect(); err != nil {
		return err
    }
    // 省略
    // 注册
	if err = s.opts.RegisterCheck(s.opts.Context); err != nil {
		log.Logf("Server %s-%s register check error: %s", config.Name, config.Id, err)
	} else {
		// announce self to the world
		if err = s.Register(); err != nil {
			log.Log("Server %s-%s register error: %s", config.Name, config.Id, err)
		}
	}
}
```
先看初始化`broker`连接的代码,这个方法的功能是启动broker服务
```go
func (h *httpBroker) Connect() error {
	h.RLock()
	if h.running {
		h.RUnlock()
		return nil
	}
	h.RUnlock()

	h.Lock()
	defer h.Unlock()

	var l net.Listener
	var err error
    // 是否为加密协议
	if h.opts.Secure || h.opts.TLSConfig != nil {
		config := h.opts.TLSConfig

		fn := func(addr string) (net.Listener, error) {
			if config == nil {
				hosts := []string{addr}

				// check if its a valid host:port
				if host, _, err := net.SplitHostPort(addr); err == nil {
					if len(host) == 0 {
						hosts = maddr.IPs()
					} else {
						hosts = []string{host}
					}
				}

				// generate a certificate
				cert, err := mls.Certificate(hosts...)
				if err != nil {
					return nil, err
				}
				config = &tls.Config{Certificates: []tls.Certificate{cert}}
			}
			return tls.Listen("tcp", addr, config)
		}

		l, err = mnet.Listen(h.address, fn)
	} else {
        // 这里的addr如果是空或者为0系统就会自动分配一个端口来供使用
        // 默认也是这样的
		fn := func(addr string) (net.Listener, error) {
			return net.Listen("tcp", addr)
		}

		l, err = mnet.Listen(h.address, fn)

	}
	if err != nil {
		return err
	}
	
	addr := h.address
	h.address = l.Addr().String()
    // 启动broker服务
    // Serve需要两个参数
    // 第一个参数需要实现net.Listener这个接口
    // 第二个参数需要实现http.Handler这个接口
    // h.mux http.Servermux ServeMux是一个HTTP请求多路复用器。它根据已注册模式列表匹配每个传入请求的URL，并调用与URL最匹配的模式的处理程序
	go http.Serve(l, h.mux)
	go func() {
        // 持续注册broker
		h.run(l)
		h.Lock()
		h.address = addr
		h.Unlock()
	}()

	// 获取注册中心
	reg, ok := h.opts.Context.Value(registryKey).(registry.Registry)
	if !ok {
		reg = registry.DefaultRegistry
	}
	// set cache
	h.r = cache.New(reg)

	// set running
	h.running = true
	return nil
}
```
httpBroker有一个`ServeHTTP`方法，这个函数实现了对广播消息的处理，这个方法实现了http.Handler接口

```go
func (h *httpBroker) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    // 请求方法只可以是POST
	if req.Method != "POST" {
		err := merr.BadRequest("go.micro.broker", "Method not allowed")
		http.Error(w, err.Error(), http.StatusMethodNotAllowed)
		return
	}
	defer req.Body.Close()
    // 解析请求表单
	req.ParseForm()

	b, err := ioutil.ReadAll(req.Body)
	if err != nil {
		errr := merr.InternalServerError("go.micro.broker", "Error reading request body: %v", err)
		w.WriteHeader(500)
		w.Write([]byte(errr.Error()))
		return
	}

	var m *Message
    // 解码消息
	if err = h.opts.Codec.Unmarshal(b, &m); err != nil {
		errr := merr.InternalServerError("go.micro.broker", "Error parsing request body: %v", err)
		w.WriteHeader(500)
		w.Write([]byte(errr.Error()))
		return
	}
    // 获取访问的订阅的服务名称
	topic := m.Header[":topic"]
	delete(m.Header, ":topic")

	if len(topic) == 0 {
		errr := merr.InternalServerError("go.micro.broker", "Topic not found")
		w.WriteHeader(500)
		w.Write([]byte(errr.Error()))
		return
	}
    // 
	p := &httpPublication{m: m, t: topic}
	id := req.Form.Get("id")

    h.RLock()
    // 这里就是处理消息事件的地方了
    // 所有的事件处理函数存储在subscribers中，然后接收到消息时，从这里面取出匹配的handler
	for _, subscriber := range h.subscribers[topic] {
		if id == subscriber.id {
			// sub is sync; crufty rate limiting
			// so we don't hose the cpu
			subscriber.fn(p)
		}
	}
	h.RUnlock()
}
```
下面看注册函数对订阅方法的处理
```go
func (s *rpcServer) Register() error {
    // 省略前面
	s.registered = true
    // s.subscribers 是在初始化订阅信息时将订阅的信息全部在这里面存放着
	for sb, _ := range s.subscribers {
        // 创建处理订阅处理消息的handler
		handler := s.createSubHandler(sb, s.opts)
		var opts []broker.SubscribeOption
		if queue := sb.Options().Queue; len(queue) > 0 {
			opts = append(opts, broker.Queue(queue))
		}

		if cx := sb.Options().Context; cx != nil {
			opts = append(opts, broker.SubscribeContext(cx))
		}

		if !sb.Options().AutoAck {
			opts = append(opts, broker.DisableAutoAck())
		}
        // 这个函数实现了将事件处理的函数注册到注册中心，并将事件处理函数handler
        // 存储到broker的httpBroker.subscribers结构中
        // 如果请求来的时候，ServeHTTP就会选择一个合适的handler来处理
		sub, err := config.Broker.Subscribe(sb.Topic(), handler, opts...)
		if err != nil {
			return err
		}
		s.subscribers[sb] = []broker.Subscriber{sub}
	}
}
```
这就是订阅事件的准备过程了，下面看发布一个消息的事件

## 发布一个消息
```go
// new一个发布
Pub = micro.NewPublisher("topic_srv_name", cient)
if err = Pub.Publish(ctx, exmsg); err != nil {
		logging.Errorf("Publish Err: %v", err)
	}
```
查看`NewPublisher`这个函数返回一个接口
```go
type Publisher interface {
	Publish(ctx context.Context, msg interface{}, opts ...client.PublishOption) error
}
```
这个是用来发布消息的接口
实际上NewPublisher返回的是micro.publisher这个结构体
```go
type publisher struct {
	c     client.Client
	topic string
}
func (p *publisher) Publish(ctx context.Context, msg interface{}, opts ...client.PublishOption) error {
	return p.c.Publish(ctx, p.c.NewMessage(p.topic, msg), opts...)
}
```
包含了订阅的消息，和客户端
下俩就是发布一个消息了
```go
if err = Pub.Publish(ctx, pubmsg); err != nil {
	logging.Errorf("Publish Err: %v", err)
}
```
`Publish`的参数是变参，前两个是固定的`ctx`和发布消息的`struct`
查看Publish方法，可以看到实际调用的是client的Publish方法，这个方法的第一个参数是context，第二个参数是Client.Message
```go
// Message is the interface for publishing asynchronously
type Message interface {
	Topic() string
	Payload() interface{}
	ContentType() string
}
```
这个接口实现了三个方法，`Topic`是获取订阅的名称，`Payload`是发布的消息，`ContextType`第三个是消息的类型
由`client`的`NewMessage`包装传入的参数，来实现`Message`这个接口,
这时最终调用的新建发布消息的函数
```go
func newMessage(topic string, payload interface{}, contentType string, opts ...MessageOption) Message {
	var options MessageOptions
	for _, o := range opts {
		o(&options)
	}

	if len(options.ContentType) > 0 {
		contentType = options.ContentType
	}

	return &message{
		payload:     payload,
		topic:       topic,
		contentType: contentType,
	}
}
```
将消息拆分放在了私有的结构体中，然后返回这个实现了Message接口的结构体
待发布的消息准备就绪后就到了发布消息的时候了
```go
func (r *rpcClient) Publish(ctx context.Context, msg Message, opts ...PublishOption) error {}
```
`client`中的`Publish`先将信息包装到`broker.Message`然后调用`broker`的`Publish`方法,这个函数才是最底层的实现发布消息的功能
```go
func (h *httpBroker) Publish(topic string, msg *Message, opts ...PublishOption) error {
	// 创建消息
	m := &Message{
		Header: make(map[string]string),
		Body:   msg.Body,
	}

	for k, v := range msg.Header {
		m.Header[k] = v
	}

	m.Header[":topic"] = topic

	// 编码消息
	b, err := h.opts.Codec.Marshal(m)
	if err != nil {
		return err
	}

	// 发布的消息编码成byte后存储到index中去
	h.saveMessage(topic, b)

	// 获取topic服务
	h.RLock()
	s, err := h.r.GetService("topic:" + topic)
	if err != nil {
		h.RUnlock()
		// ignore error
		return nil
	}
	h.RUnlock()

    // 请求的函数
	pub := func(node *registry.Node, t string, b []byte) error {
		scheme := "http"

		// check if secure is added in metadata
		if node.Metadata["secure"] == "true" {
			scheme = "https"
		}

		vals := url.Values{}
		vals.Add("id", node.Id)
        // 生成请求的URL
		uri := fmt.Sprintf("%s://%s:%d%s?%s", scheme, node.Address, node.Port, DefaultSubPath, vals.Encode())
		r, err := h.c.Post(uri, "application/json", bytes.NewReader(b))
		if err != nil {
			return err
		}

		// discard response body
		io.Copy(ioutil.Discard, r.Body)
		r.Body.Close()
		return nil
	}
    // 选择node 由两种方法一种是广播 一种是随机选择一个node
	srv := func(s []*registry.Service, b []byte) {
		for _, service := range s {
			// only process if we have nodes
			if len(service.Nodes) == 0 {
				continue
			}

			switch service.Version {
			// 广播意味着发不到所有的node里
			case broadcastVersion:
				var success bool

				// publish to all nodes
				for _, node := range service.Nodes {
					// publish async
					if err := pub(node, topic, b); err == nil {
						success = true
					}
				}

				// 发送失败就重新将待发送的消息放入inbox
				if !success {
					h.saveMessage(topic, b)
                }
                // 如果设置了消息队列就随机选择一个节点
			default:
				// 随机选择一个节点
				node := service.Nodes[rand.Int()%len(service.Nodes)]

				// 发布消息到一个节点
				if err := pub(node, topic, b); err != nil {
					// 发送失败就重新将待发送的消息放入inbox
					h.saveMessage(topic, b)
				}
			}
		}
	}

	// do the rest async
	/// 异步发送消息
	go func() {
		// get a third of the backlog
		messages := h.getMessage(topic, 8)
		delay := (len(messages) > 1)

		// 循环发送所有的消息
		for _, msg := range messages {
			// 发布消息
			srv(s, msg)

			// 如果有多个消息 阻塞一会后再发送接收到的消息
			if delay {
				time.Sleep(time.Millisecond * 100)
			}
		}
	}()

	return nil
}
```