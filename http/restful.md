RESTful 架构详解

## 协议
API与用户的通信协议使用`HTTPS`
## 域名
应该尽量将API部署在专门域名之下
## 版本
应该将API的版本号放入URL
## 路径
在RESTful架构中，每一种网址代表一个资源，所有网址中只能有名词
## HTTP动词
常用的HTTP动词有下面五个（括号里是对应的SQL命令）。
- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
- DELETE（DELETE）：从服务器删除资源。
## 过滤信息
如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。
## 状态码
服务器向用户返回的状态码和提示信息
## 错误处理（Error handling）
## 返回结果
针对不同操作，服务器向用户返回的结果应该符合以下规范。

- GET /collection：返回资源对象的列表（数组）
- GET /collection/resource：返回单个资源对象
- POST /collection：返回新生成的资源对象
- PUT /collection/resource：返回完整的资源对象
- PATCH /collection/resource：返回完整的资源对象
- DELETE /collection/resource：返回一个空文档