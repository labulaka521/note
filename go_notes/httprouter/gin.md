## `Gin`请求过程分析

[Gin](github.com/gin-gonic/gin)在路由管理使用了基于`radix tree`的路由框架[httprouter](https://github.com/julienschmidt/httprouter),
```go
r := gin.New()
r.Use(gin.Logger(), gin.Recovery())
r1 = r.Group("/actuator")
```
`gin.New`是创建一个`Engine`实例,这是此框架的核心，包含了框架运维性的一些配置，

```go
type Engine struct {
    // 
	RouterGroup

	// 自动重定向
	RedirectTrailingSlash bool

	// 自动修复路径
	RedirectFixedPath bool

    // 如果true，当路由没有被命中，去检查是否其他Method命中
    // 如果命中，响应405，如果没有命中，请求将由Not Found handler 来处理
	HandleMethodNotAllowed bool
	
    ForwardedByClientIP    bool
    
	AppEngine bool

	UseRawPath bool

	UnescapePathValues bool

	MaxMultipartMemory int64

	delims           render.Delims
	secureJsonPrefix string
	HTMLRender       render.HTMLRender
	FuncMap          template.FuncMap
	allNoRoute       HandlersChain
	allNoMethod      HandlersChain
	noRoute          HandlersChain
	noMethod         HandlersChain
	// 对象池用来复用Context对象 减少gc的压力
    pool             sync.Pool
    // 每个请求方法一个 trees
	trees            methodTrees
}
```

`RouterGroup`可以用来规划路由组，并为一些组内的所有handle统一中间件，
这是RouterGroup的结构，Router实现了`IRouter`接口，这个接口实现了各种请求方法和路由组划分
```go
type RouterGroup struct {
    // 保存handler的切片
	Handlers HandlersChain
	// 路由前缀
    basePath string
    // 每一个分组都保存着相同的Engine 这是为了将分组里的url保存到Engine的trees中去
    engine   *Engine
    // 是否为root节点
	root     bool
}
```

可以看见`RouterGroup`和`Engine`相互嵌套，这样Engine也就有了`RouterGroup`的方法    
`Group()`用来创建一个路由组
```go
func (group *RouterGroup) Group(relativePath string, handlers ...HandlerFunc) *RouterGroup {
	return &RouterGroup{
        // 新的路由组继承了以前的的公共handle和创建时传入的handler
        Handlers: group.combineHandlers(handlers),
        // 绝对路径
        basePath: group.calculateAbsolutePath(relativePath),
        // 将原来的Engine复制过来，以便在这个组下添加的请求handler可以添加到engine的trees中去
		engine:   group.engine,
	}
}
```
`Group`创建了一个新的路由组，这个路由组包含了原先创建的`Engine`，然后路由组里添加的`handle`最终由[httprouter](https://github.com/julienschmidt/httprouter)这个框架添加到`Engine`的`trees`中  
现在来看一下路由的添加过程
```go
r.GET("/test",test.GetData)

func (group *RouterGroup) GET(relativePath string, handlers ...HandlerFunc) IRoutes {
	return group.handle("GET", relativePath, handlers)
}
// 添加handle
func (group *RouterGroup) handle(httpMethod, relativePath string, handlers HandlersChain) IRoutes {
    absolutePath := group.calculateAbsolutePath(relativePath)
    // 新的路由组继承了以前的的公共handle和创建时传入的handler
    handlers = group.combineHandlers(handlers)
    // 添加路由 这步是使用httprouter框架完成的 将当前handle添加到Engine的trees中
    group.engine.addRoute(httpMethod, absolutePath, handlers)
    // 如果是root节点返回Engine 如果是不是root返回RouterGroup
	return group.returnObj()
}
```
所以总结就是每添加一个请求handle就会把前面所有公共的handler复制一遍，和传入的的一起挂在路由下，等请求来的时候从上往下依次运行，

## 接收请求

```go
func (engine *Engine) Run(addr ...string) (err error) {
	defer func() { debugPrintError(err) }()
	address := resolveAddress(addr)
	debugPrint("Listening and serving HTTP on %s\n", address)
	err = http.ListenAndServe(address, engine)
	return
}
```
还是调用的go的http自带的方法`err = http.ListenAndServe(address, engine)`
这个函数需要两个参数一个是启动地址，另一个是实现了`http.Handler`接口的，而`Engine`就实现了这个接口
```go
func (engine *Engine) ServeHTTP(w http.ResponseWriter, req *http.Request) {
	// 从对象池中获取一个context对象，如果没有对象就创建一个只包含Engine的context对象
	c := engine.pool.Get().(*Context)
	c.writermem.reset(w)
	// 设置请求的数据
	c.Request = req
	// 初始化Context对象
	c.reset()
	// 处理请求
	// 这一步会去trees中寻找对应路由的handler，然后运行
	engine.handleHTTPRequest(c)
	// 请求完毕后又将context对象放入请求池 减少垃圾回收的压力
	engine.pool.Put(c)
}
```
然后启动时候程序就会等待请求，然后处理请求
```go
func (engine *Engine) handleHTTPRequest(c *Context) {
	// 请求方法
	httpMethod := c.Request.Method
	rPath := c.Request.URL.Path
	unescape := false
	if engine.UseRawPath && len(c.Request.URL.RawPath) > 0 {
		rPath = c.Request.URL.RawPath
		unescape = engine.UnescapePathValues
	}
	rPath = cleanPath(rPath)

	// tress每个请求方法都是一颗新的树
	// 这里会循环每一棵树然后找到对应的handler
	t := engine.trees
	for i, tl := 0, len(t); i < tl; i++ {
		if t[i].method != httpMethod {
			continue
		}
		root := t[i].root
		// 在树中寻找路由
		handlers, params, tsr := root.getValue(rPath, c.Params, unescape)
		if handlers != nil {
			// 寻找到对应的路由后会讲路由上挂载的信息放在Context这个结构中去
			c.handlers = handlers
			// 路由参数
			c.Params = params
			// 执行handle
			c.Next()
			c.writermem.WriteHeaderNow()
			return
		}
		if httpMethod != "CONNECT" && rPath != "/" {
			if tsr && engine.RedirectTrailingSlash {
				redirectTrailingSlash(c)
				return
			}
			if engine.RedirectFixedPath && redirectFixedPath(c, root, engine.RedirectFixedPath) {
				return
			}
		}
		break
	}
	// 是否检查这个url的其他handler
	// 如果找到会返回状态吗405
	if engine.HandleMethodNotAllowed {
		for _, tree := range engine.trees {
			if tree.method == httpMethod {
				continue
			}
			if handlers, _, _ := tree.root.getValue(rPath, nil, unescape); handlers != nil {
				c.handlers = engine.allNoMethod
				serveError(c, http.StatusMethodNotAllowed, default405Body)
				return
			}
		}
	}
	// 返回状态吗404
	c.handlers = engine.allNoRoute
	serveError(c, http.StatusNotFound, default404Body)
}
```
`handleHTTPRequest`主要的功能就是寻找路由，如果寻找到了就将路由的参数和handler放在Context这个上下文中，然后通过`c.Next`执行所有的handler

```go
func (c *Context) Next() {
	c.index++
	for c.index < int8(len(c.handlers)) {
		// 执行handler
		// c.handlers[c.index] 获取middle 每个middle的参数是Context
		c.handlers[c.index](c)
		c.index++
	}
}
```
当运行第一个handler这是这个路由最外层的middle，每个middle中必须包含一个`c.Next`来处理接下来的流程，Context初始化index为-1，然后进入第一个middle时，会加+1，然后判断当前index是否大于handler的总数，如果没有大于就取得一个handler `c.handlers[c.index](c)`，然后传入Context运行，然后直到最后一个真正处理业务逻辑的handler后，将执行的结果响应，当请求响应后，然后会把响应的请求的，重新放入连接池，这样做的目的就是为了对象复用减轻gc的压力

