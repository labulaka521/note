`Gin`路由分析

[Gin](github.com/gin-gonic/gin)在路由管理使用了基于`radix tree`的路由框架[httprouter](https://github.com/julienschmidt/httprouter),
```go
r := gin.New()
r.Use(gin.Logger(), gin.Recovery())
r1 = r.Group("/actuator")
```
`gin.New`是创建一个`Engine`实例  
这是此框架的核心，包含了框架需要运行的全部配置

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
    pool             sync.Pool
    // 每个请求方法一个 trees
	trees            methodTrees
}
```

`RouterGroup`可以用来方便的统一路由组是统一前缀和为一些指定前缀的URL添加中间件，
这是RouterGroup的结构，Router实现了`IRouter`接口，这个接口
```go
type RouterGroup struct {
    // 保存handler的切片
	Handlers HandlersChain
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
        // 以前的所有公共handler
        Handlers: group.combineHandlers(handlers),
        // 绝对路径
        basePath: group.calculateAbsolutePath(relativePath),
        // 将原来的Engine复制过来
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
    // 计算handle的路径
    absolutePath := group.calculateAbsolutePath(relativePath)
    // 路由的handle
    handlers = group.combineHandlers(handlers)
    // 添加路由 这步是使用httprouter框架完成的 将当前handle添加到Engine的trees中
    group.engine.addRoute(httpMethod, absolutePath, handlers)
    // 如果是root节点返回Engine 如果是不是root返回RouterGroup
	return group.returnObj()
}
```


