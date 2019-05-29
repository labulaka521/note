# http

使用http写一个server
```go
func main() {
	http.HandleFunc("/",Index)

	log.Fatal(http.ListenAndServe(":8080", nil))
}

func Index(w http.ResponseWriter, r *http.Request){
	fmt.Fprint(w,"Hello")
}
```

`http.HandleFunc` 将路径`/`与处理函数`Index` 通过`DefaultServeMux.HandleFunc`函数通过调用`Handle`注册到了结构体 `ServeMux`的m中  


```go
type ServeMux struct {
	mu    sync.RWMutex
	m     map[string]muxEntry
	hosts bool // whether any patterns contain hostnames
}
```

```go
var defaultServeMux ServeMux
// DefaultServeMux is the default ServeMux used by Serve.
var DefaultServeMux = &defaultServeMux

var mux *ServeMux
```

注册路径与Hanlder调用链  
```
http.HandleFunc(pattern, handler) --> DefaultServeMux.HandleFunc(pattern, handler) --> mux.Handle(pattern, HandlerFunc(handler))   
```
然后在`Handler`中将路径`pattern`和Handler注册到`ServeMux`的`m`中，等待HTTP请求。


```go
// A Handler responds to an HTTP request.
//
type Handler interface {
	ServeHTTP(ResponseWriter, *Request)
}
```
当在处理HTTP请求的时候，会调用`Handler`接口的`ServeHTTP`方法,而`ServeMux`也实现了`ServeHTTP`方法
```go
func (mux *ServeMux) ServeHTTP(w ResponseWriter, r *Request) {
	if r.RequestURI == "*" {
		if r.ProtoAtLeast(1, 1) {
			w.Header().Set("Connection", "close")
		}
		w.WriteHeader(StatusBadRequest)
		return
	}
	h, _ := mux.Handler(r)
	h.ServeHTTP(w, r)
}
```
HTTP请求时的调用链
```
HTTP请求 --> Handler 接口 ServeHTTP函数 - > ServeMux的ServeHTTP函数 -> 注册的函数Index
```