## HTTP 的 Keep-Alive模式
当使用普通模式时，即非`KeepAlive`模式时，每个请求/应答都需要新建一个连接，数据传输完成后立即断开连接；当使用`Keep-Alive`模式时，这个模式时客户端和服务端的连接是在数据传输完成后是不中断的，当后续又有请求时，可以复用连接
![](../image/keepalive.png)

如何判断请求所得到的响应数据已经接受完成
- 使用消息首部字段`Conent-Length`  
  表示实体内容长度，客户端可以根据这个值来判断数据是否接受完成
- 使用消息首部字段`Transfer-Encoding`  
  在传输一些动态页面时，服务器是与现实不知道内容大小，这时就可以使用`Transfer-Encoding: chunk`模式来传输数据。即如果要一边生产数据，一边发送数据给请求端，就要使用`Transfer-Encoding:chunked`这样的方式来代替`Conteng-Length`。chunk编码将数据分为一块一块的发生。Chunked编码将使用若干个Chunk串连而成，由一个标明长度为0的chunk标识结束。
