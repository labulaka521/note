# RPC调用源码

## 注册handler
注册handler这个文件是由proto文件生成的*.micro.go文件主要目的是将handler注册到创建的server中，
```go
func RegisterActuatorHandler(s server.Server, hdlr ActuatorHandler, opts ...server.HandlerOption) error {
	type actuator interface {
		CreateActuator(ctx context.Context, in *Actuat, out *Response) error
		DeleteActuator(ctx context.Context, in *Actuat, out *Response) error
		ChangeActuator(ctx context.Context, in *Actuat, out *Response) error
		GetActuator(ctx context.Context, in *Actuat, out *Response) error
		GetAllExecutorIP(ctx context.Context, in *Actuat, out *Response) error
	}
	type Actuator struct {
		actuator
	}
	h := &actuatorHandler{hdlr}
	return s.Handle(s.NewHandler(&Actuator{h}, opts...))
}
```
先看`s.NewHandler`这个函数，这个方法返回一个接口`server.Handler`
```go
type Handler interface {
    // proto文件里服务的名称
    Name() string
    // 实现服务接口的结构体 也就是在注册时传入的值
    Handler() interface{}
    // 服务的所有方法
    Endpoints() []*registry.Endpoint
    // 请求handler的配置选项
	Options() HandlerOptions
}
```
这个接口是处理请求handle，函数的调用链
```
s.NewHandler   
  - s.router.NewHandler
  - newRpcHandler
```
newRpchandler通过反射将传入的struct的方法提取出来放在`rpcHandler`这个结构体中，这个结构体实现了`server.Handler`这个接口，

```go
func newRpcHandler(handler interface{}, opts ...HandlerOption) Handler {
	options := HandlerOptions{
		Metadata: make(map[string]map[string]string),
	}

	for _, o := range opts {
		o(&options)
	}

	typ := reflect.TypeOf(handler)
	hdlr := reflect.ValueOf(handler)
	name := reflect.Indirect(hdlr).Type().Name()

	var endpoints []*registry.Endpoint

	for m := 0; m < typ.NumMethod(); m++ {
		if e := extractEndpoint(typ.Method(m)); e != nil {
			e.Name = name + "." + e.Name

			for k, v := range options.Metadata[e.Name] {
				e.Metadata[k] = v
			}

			endpoints = append(endpoints, e)
		}
	}

	return &rpcHandler{
		name:      name,
		handler:   handler,
		endpoints: endpoints,
		opts:      options,
	}
}
```
下面是Handle方法这个函数先把，所有的方法通过反射取出所有的参数、类型等信息保存在router中的serviceMap中，然后再将路由保存在服务的handlers中
```go
func (s *rpcServer) Handle(h Handler) error {
	s.Lock()
	defer s.Unlock()
    // 将所有的方法保存在路由中
	if err := s.router.Handle(h); err != nil {
		return err
	}
    // 记录handler
	s.handlers[h.Name()] = h

	return nil
}
```
进入route.Handle,最终handle信息通过反射得到所有的方法后，放在了serviceMap中，具体的方法是放在了`methodType`这个结构体中，这个结构体定义了保存了方法的参数，类型等各种类型
```go
func (router *router) Handle(h Handler) error {
	router.mu.Lock()
	defer router.mu.Unlock()
	if router.serviceMap == nil {
		router.serviceMap = make(map[string]*service)
	}

	if len(h.Name()) == 0 {
		return errors.New("rpc.Handle: handler has no name")
	}
	if !isExported(h.Name()) {
		return errors.New("rpc.Handle: type " + h.Name() + " is not exported")
	}

	rcvr := h.Handler()
	s := new(service)
	s.typ = reflect.TypeOf(rcvr)
	s.rcvr = reflect.ValueOf(rcvr)

	// 检查是否已经保存
	if _, present := router.serviceMap[h.Name()]; present {
		return errors.New("rpc.Handle: service already defined: " + h.Name())
	}

	s.name = h.Name()
	s.method = make(map[string]*methodType)

	// 将所有的方法提取出来
	for m := 0; m < s.typ.NumMethod(); m++ {
		// 方法
		method := s.typ.Method(m)
		// 提取
		if mt := prepareMethod(method); mt != nil {
			s.method[method.Name] = mt
		}
	}

	// 检查方法是否实现
	if len(s.method) == 0 {
		return errors.New("rpc Register: type " + s.name + " has no exported methods of suitable type")
	}

	// 将方法的各种参数保存在这个结构中去
	router.serviceMap[s.name] = s
	return nil
}
```
总体来说就是将实现了接口的所有方法注册到新建的server里，然后供后面的启动，请求使用

## 启动服务等待连接
查看`server.Run`方法进入这个方法里，最终调用的是`server.rpcServer`中的`Start`方法，
```go
func (s *rpcServer) Start() error {
	registerDebugHandler(s)
    config := s.Options()

    // 启动transport监听
    // transport是用来服务与服务之间同步请求/响应的通信接口
	ts, err := config.Transport.Listen(config.Address)
	if err != nil {
		return err
    }
    // 省略
	go func() {
		for {
            // 接收连接
            // ServerConn是处理连接的函数
            // 启动transport服务
            // 接收到client的请求后调用请求的函数处理请求
            // 这里就实现了等待调用方调用请求
			err := ts.Accept(s.ServeConn)

			// TODO: listen for messages
			// msg := broker.Exchange(service).Consume()

			select {
			// 退出通道
			case <-exit:
				return
			// 检查err 
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
    
}
```

## 客户端调用过程

创建客户端，返回由proto生成的服务接口`JobService`
```go
JobClient = pbjob.NewJobService("xxx.srv.name", client.DefaultClient)
```
这个创建的代码在`job.micro.go` 中是由micro自动生成的代码
```go
func NewJobService(name string, c client.Client) JobService {
    // 传入的client为空将使用默认的client
	if c == nil {
		c = client.NewClient()
    }
    // 
	if len(name) == 0 {
		name = "crocodile.srv.job"
	}
	return &jobService{
		c:    c,
		name: name,
	}
}
```
`jobService`实现了`JobService`接口
```go
type jobService struct {
    // 客户端
    c    client.Client
    // 服务的名称
	name string
}
```
看一下定义的方法,这个是`proto`文件里定义的方法，由`proto`命令自动生成的代码
```go
func (c *jobService) CreateJob(ctx context.Context, in *Task, opts ...client.CallOption) (*Response, error) {
    // 新建一个请求
    // 最终调用的是client的newRequest函数
    // 这个函数将请求需要的服务名 方法名，请求数据等放在rpcRequest这个结构体中返回
    req := c.c.NewRequest(c.name, "Job.CreateJob", in)
    // new一个新的响应
    out := new(Response)
    // 请求的函数
	err := c.c.Call(ctx, req, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}
```
下来看一下Call这个函数，客户端调用服务的时候可以传入指定的选项,这个函数先选择一个node，然后去调用，调用的时候可以使用重试的机制保证客户端调用正常返回
```go
// 调用
func (r *rpcClient) Call(ctx context.Context, request Request, response interface{}, opts ...CallOption) error {
	// 赋值
	callOpts := r.opts.CallOptions
	for _, opt := range opts {
		opt(&callOpts)
	}
    // 选择一个node来执行调用 这个返回的是一个函数
	next, err := r.next(request, callOpts)
	if err != nil {
		return err
	}

	// check if we already have a deadline
	d, ok := ctx.Deadline()
	if !ok {
		// 如果没有截止时间就创建一个
		ctx, _ = context.WithTimeout(ctx, callOpts.RequestTimeout)
	} else {
		// got a deadline so no need to setup context
        // but we need to set the timeout we pass along
        // 设置请求超时时长
		opt := WithRequestTimeout(d.Sub(time.Now()))
		opt(&callOpts)
	}

	// should we noop right here?
	select {
	case <-ctx.Done():
		return errors.Timeout("go.micro.client", fmt.Sprintf("%v", ctx.Err()))
	default:
	}

	// 赋值调用服务 调用call
	rcall := r.call

	// wrap the call in reverse
	for i := len(callOpts.CallWrappers); i > 0; i-- {
		rcall = callOpts.CallWrappers[i-1](rcall)
	}

    // return errors.New("go.micro.client", "request timeout", 408)
    // 包装请求客户端
	call := func(i int) error {
		// call backoff first. Someone may want an initial start delay
		t, err := callOpts.Backoff(ctx, request, i)
		if err != nil {
			return errors.InternalServerError("go.micro.client", "backoff error: %v", err.Error())
		}

		// only sleep if greater than 0
		if t.Seconds() > 0 {
			time.Sleep(t)
		}

		// 获取node的信息
		node, err := next()
		if err != nil && err == selector.ErrNotFound {
			return errors.NotFound("go.micro.client", "service %s: %v", request.Service(), err.Error())
		} else if err != nil {
			return errors.InternalServerError("go.micro.client", "error getting next %s node: %v", request.Service(), err.Error())
		}

		// make the call
		err = rcall(ctx, node, request, response, callOpts)
		r.opts.Selector.Mark(request.Service(), node, err)
		return err
	}

	ch := make(chan error, callOpts.Retries+1)
	var gerr error
    // 调用服务
    // Retires是重试次数
    // 客户端可以设置请求重试次数，防止请求时服务挂掉
    // 这里只有调用服务时，返回了错误才会重试
	for i := 0; i <= callOpts.Retries; i++ {
		go func(i int) {
			ch <- call(i)
		}(i)

		select {
        case <-ctx.Done():
            // 超时退出
			return errors.Timeout("go.micro.client", fmt.Sprintf("call timeout: %v", ctx.Err()))
		case err := <-ch:
			// if the call succeeded lets bail early
			if err == nil {
				return nil
			}
            // 重试函数 
            // 默认的重试函数是一个RetryOnError这个函数
            // 这个函数只有在响应code是408 和500 超时和服务端错误才会重试
            retry, rerr := callOpts.Retry(ctx, request, i, err)
            // err不等于nil就直接返回了
			if rerr != nil {
				return rerr
			}
            // 如果retry为false就直接返回退出
			if !retry {
				return err
			}

			gerr = err
		}
	}

	return gerr
}
```
这是选择node的方法next 具体如果指定了服务端的地址，就使用直接返回这个指定的node，如果没有设置就使用selector来选择一个node，返回的值是函数这个函数返回一个node和一个err
```go
type Next func() (*registry.Node, error)
```
这就是选择node的代码
```go
func (r *rpcClient) next(request Request, opts CallOptions) (selector.Next, error) {
	service := request.Service()

	// get proxy
	if prx := os.Getenv("MICRO_PROXY"); len(prx) > 0 {
		service = prx
	}

	// get proxy address
	if prx := os.Getenv("MICRO_PROXY_ADDRESS"); len(prx) > 0 {
		opts.Address = prx
	}

	// 如果设置了调用服务的地址就返回指定的node
	if len(opts.Address) > 0 {
		address := opts.Address
		port := 0

		host, sport, err := net.SplitHostPort(opts.Address)
		if err == nil {
			address = host
			port, _ = strconv.Atoi(sport)
		}

		return func() (*registry.Node, error) {
			return &registry.Node{
				Address: address,
				Port:    port,
			}, nil
		}, nil
	}

    // 从Selectot中选择一个node
    // 
	next, err := r.opts.Selector.Select(service, opts.SelectOptions...)
	if err != nil && err == selector.ErrNotFound {
		return nil, errors.NotFound("go.micro.client", "service %s: %v", service, err.Error())
	} else if err != nil {
		return nil, errors.InternalServerError("go.micro.client", "error selecting %s node: %v", service, err.Error())
	}

	return next, nil
}
```
最终的调用服务是rpcClient的私有方法`call`
```go
func (r *rpcClient) call(ctx context.Context, node *registry.Node, req Request, resp interface{}, opts CallOptions) error {
    //  已经选择的服务地址
	address := node.Address
	if node.Port > 0 {
		address = fmt.Sprintf("%s:%d", address, node.Port)
	}
    // 通信的消息
	msg := &transport.Message{
		Header: make(map[string]string),
	}

	md, ok := metadata.FromContext(ctx)
	if ok {
		for k, v := range md {
			msg.Header[k] = v
		}
	}

	// 设置超时时间
	msg.Header["Timeout"] = fmt.Sprintf("%d", opts.RequestTimeout)
	// set the content type for the request
	msg.Header["Content-Type"] = req.ContentType()
	// set the accept header
	msg.Header["Accept"] = req.ContentType()

	// 解码
	cf := setupProtocol(msg, node)

	// no codec specified
	if cf == nil {
		var err error
		cf, err = r.newCodec(req.ContentType())
		if err != nil {
			return errors.InternalServerError("go.micro.client", err.Error())
		}
	}

	var grr error
    // 与服务端建立连接
	c, err := r.pool.getConn(address, r.opts.Transport, transport.WithTimeout(opts.DialTimeout))
	if err != nil {
		return errors.InternalServerError("go.micro.client", "connection error: %v", err)
	}
	defer func() {
		// defer execution of release
		r.pool.release(address, c, grr)
	}()

	seq := atomic.LoadUint64(&r.seq)
	atomic.AddUint64(&r.seq, 1)
	codec := newRpcCodec(msg, c, cf)

	rsp := &rpcResponse{
		socket: c,
		codec:  codec,
	}

	stream := &rpcStream{
		context:  ctx,
		request:  req,
		response: rsp,
		codec:    codec,
		closed:   make(chan bool),
		id:       fmt.Sprintf("%v", seq),
	}
	defer stream.Close()

	ch := make(chan error, 1)

	go func() {
		defer func() {
			if r := recover(); r != nil {
				ch <- errors.InternalServerError("go.micro.client", "panic recovered: %v", r)
			}
		}()

		// 发送请求数据
		if err := stream.Send(req.Body()); err != nil {
			ch <- err
			return
		}

		// 接收响应数据
		if err := stream.Recv(resp); err != nil {
			ch <- err
			return
		}

		// success
		ch <- nil
	}()

	select {
	case err := <-ch:
		grr = err
		return err
	case <-ctx.Done():
		grr = ctx.Err()
		return errors.Timeout("go.micro.client", fmt.Sprintf("%v", ctx.Err()))
	}
}
```
请求指定方法封装参数->编码数据->请求连接->发送数据->接收响应数据

创建一个定义的服务--> newRequest封装请求数据-->选择node节点-->编码数据-->调用服务(失败重试)

## 服务端响应
服务端接收客户端请求
服务启动以后程序就会在这里等待连接
```go
// listen for connections
err := ts.Accept(s.ServeConn)
```
ts.Accept实现了一个handler这个会处理所有的请求，
```go
func (h *httpTransportListener) Accept(fn func(Socket)) error {
	//  创建一个请求多路复用器
	mux := http.NewServeMux()

	// 请求多路复用器是匹配所有的相似的路由所以这个的url路由是/所以会匹配所有的请求
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		var buf *bufio.ReadWriter
		var con net.Conn

		// 请求协议
		if r.ProtoMajor == 1 {
			b, err := ioutil.ReadAll(r.Body)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			r.Body = ioutil.NopCloser(bytes.NewReader(b))
			// hijack the conn
			hj, ok := w.(http.Hijacker)
			if !ok {
				// we're screwed
				http.Error(w, "cannot serve conn", http.StatusInternalServerError)
				return
			}

			conn, bufrw, err := hj.Hijack()
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			defer conn.Close()
			buf = bufrw
			con = conn
		}

		// save the request
		ch := make(chan *http.Request, 1)
		ch <- r
        // fn是传入的参数，这个
		fn(&httpTransportSocket{
			ht:     h.ht,
			w:      w,
			r:      r,
			rw:     buf,
			ch:     ch,
			conn:   con,
			local:  h.Addr(),
			remote: r.RemoteAddr,
		})
	})

	// get optional handlers
	if h.ht.opts.Context != nil {
		handlers, ok := h.ht.opts.Context.Value("http_handlers").(map[string]http.Handler)
		if ok {
			for pattern, handler := range handlers {
				mux.Handle(pattern, handler)
			}
		}
	}

	// default http2 server
	srv := &http.Server{
		Handler: mux,
	}

	// insecure connection use h2c
	if !(h.ht.opts.Secure || h.ht.opts.TLSConfig != nil) {
		srv.Handler = h2c.NewHandler(mux, &http2.Server{})
	}

	// 启动服务
	return srv.Serve(h.listener)
}
```
ts.Accept只是等待请求连接，`s.ServeConn`才是处理请求的函数。
```go
func (s *rpcServer) ServeConn(sock transport.Socket) {
	defer func() {
		// close socket
		sock.Close()

		if r := recover(); r != nil {
			log.Log("panic recovered: ", r)
			log.Log(string(debug.Stack()))
		}
	}()

	for {
		var msg transport.Message
        // 接收请求的消息
		if err := sock.Recv(&msg); err != nil {
			return
		}

		// waithroup+1
		if s.wg != nil {
			s.wg.Add(1)
		}

		// 获取服务的超时时间
		to := msg.Header["Timeout"]
		// we use this Content-Type header to identify the codec needed
		ct := msg.Header["Content-Type"]

		// 复制请求头的信息
		hdr := make(map[string]string)
		for k, v := range msg.Header {
			hdr[k] = v
		}

		// set local/remote ips
		hdr["Local"] = sock.Local()
		hdr["Remote"] = sock.Remote()

		// 创建一个新的ctx
		ctx := metadata.NewContext(context.Background(), hdr)

		// s设置服务超时时间
		if len(to) > 0 {
			if n, err := strconv.ParseUint(to, 10, 64); err == nil {
				ctx, _ = context.WithTimeout(ctx, time.Duration(n))
			}
		}

		// 请求类型
		if len(ct) == 0 {
			msg.Header["Content-Type"] = DefaultContentType
			ct = DefaultContentType
		}

		// 请求协议
		cf := setupProtocol(&msg)

		// 请求协议
		if cf == nil {
			// TODO: needs better error handling
			var err error
			if cf, err = s.newCodec(ct); err != nil {
				sock.Send(&transport.Message{
					Header: map[string]string{
						"Content-Type": "text/plain",
					},
					Body: []byte(err.Error()),
				})
				if s.wg != nil {
					s.wg.Done()
				}
				return
			}
		}

		rcodec := newRpcCodec(&msg, sock, cf)

		// 创建请求
		request := &rpcRequest{
            // 请求的服务名
            service:     getHeader("Micro-Service", msg.Header),
            // 请求的方法名
            method:      getHeader("Micro-Method", msg.Header),
            // 
			endpoint:    getHeader("Micro-Endpoint", msg.Header),
			contentType: ct,
			codec:       rcodec,
			header:      msg.Header,
			body:        msg.Body,
			socket:      sock,
			stream:      true,
		}

		// internal response
		response := &rpcResponse{
			header: make(map[string]string),
			socket: sock,
			codec:  rcodec,
		}

		// 路由信息
		r := s.opts.Router

		// if nil use default router
		if s.opts.Router == nil {
			r = s.router
		}

		// 创建一个包装函数
		handler := func(ctx context.Context, req Request, rsp interface{}) error {
			return r.ServeRequest(ctx, req, rsp.(Response))
		}

		for i := len(s.opts.HdlrWrappers); i > 0; i-- {
			handler = s.opts.HdlrWrappers[i-1](handler)
		}

        // TODO: handle error better
        // 请求服务端
		if err := r.ServeRequest(ctx, request, response); err != nil {
			// write an error response
			err = rcodec.Write(&codec.Message{
				Header: msg.Header,
				Error:  err.Error(),
				Type:   codec.Error,
			}, nil)
			// could not write the error response
			if err != nil {
				log.Logf("rpc: unable to write error response: %v", err)
			}
			if s.wg != nil {
				s.wg.Done()
			}
			return
		}

		// done
		if s.wg != nil {
			s.wg.Done()
		}
	}
}

```
`ServeRequest`也是为请求前作准备，这函数将请求服务，类型，等信息取出来
```go
func (router *router) ServeRequest(ctx context.Context, r Request, rsp Response) error {
    sending := new(sync.Mutex)
    //读取请求服务类型，请求数据，
    // 从router.serviceMap(这个是初始化服务的时候将所有handler保存在这个结构中)取出访问的方法的各种参数
	service, mtype, req, argv, replyv, keepReading, err := router.readRequest(r)
	if err != nil {
		if !keepReading {
			return err
		}
		// send a response if we actually managed to read a header.
		if req != nil {
			router.freeRequest(req)
		}
		return err
    }
    // 调用call方法
	return service.call(ctx, router, sending, mtype, req, argv, replyv, rsp.Codec())
}
```
这个函数准备好请求数据后请求`service.call`，这个函数才是最终执行调用写好的方法，
```go
func (s *service) call(ctx context.Context, router *router, sending *sync.Mutex, mtype *methodType, req *request, argv, replyv reflect.Value, cc codec.Writer) error {
	defer router.freeRequest(req)

	function := mtype.method.Func
	var returnValues []reflect.Value
	// 请求所需要的数据
	r := &rpcRequest{
		service:     req.msg.Target,
		contentType: req.msg.Header["Content-Type"],
		method:      req.msg.Method,
		endpoint:    req.msg.Endpoint,
		body:        req.msg.Body,
	}
	// 不是流式RPC
	if !mtype.stream {
		fn := func(ctx context.Context, req Request, rsp interface{}) error {
			returnValues = function.Call([]reflect.Value{s.rcvr, mtype.prepareContext(ctx), reflect.ValueOf(argv.Interface()), reflect.ValueOf(rsp)})

			// The return value for the method is an error.
			if err := returnValues[0].Interface(); err != nil {
				return err.(error)
			}
			return nil
		}

		// 执行handler
		if err := fn(ctx, r, replyv.Interface()); err != nil {
			return err
		}

		// 发送
		return router.sendResponse(sending, req, replyv.Interface(), cc, true)
	}

	// 流式请求
	rawStream := &rpcStream{
		context: ctx,
		codec:   cc.(codec.Codec),
		request: r,
		id:      req.msg.Id,
	}

	fn := func(ctx context.Context, req Request, stream interface{}) error {
		returnValues = function.Call([]reflect.Value{s.rcvr, mtype.prepareContext(ctx), reflect.ValueOf(stream)})
		if err := returnValues[0].Interface(); err != nil {
			// the function returned an error, we use that
			return err.(error)
		} else if serr := rawStream.Error(); serr == io.EOF || serr == io.ErrUnexpectedEOF {
			return nil
		} else {
			// no error, we send the special EOS error
			return lastStreamResponseError
		}
	}

	// client.Stream request
	r.stream = true

	// 执行handler
	return fn(ctx, r, rawStream)
}
```
服务端处理过程
ts.Accept注册transport handler, 接收请求 -> s.ServeConn 处理单次请求 接收请求的方法 -->router中找到对应的处理handler进行处理 -->发送请求的响应数据