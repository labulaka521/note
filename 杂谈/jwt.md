# JWT (JSON WEB TOKEN)

- JWT  
Json web token (JWT), 是为了在网络应用环境间传递声明而执行的一种基于JSON的开放标准（(RFC 7519).该token被设计为紧凑且安全的，特别适用于分布式站点的单点登录（SSO）场景。JWT的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该token也可直接被用于认证，也可被加密。

**基于token的鉴权机制**

基于token的鉴权机制类似于http协议也是无状态的，它不需要在服务端去保留用户的认证信息或者会话信息。这就意味着基于token认证机制的应用不需要去考虑用户在哪一台服务器登录了，这就为应用的扩展提供了便利。
流程上是这样的：

- 用户使用用户名密码来请求服务器
- 服务器进行验证用户的信息
- 服务器通过验证发送给用户一个token
- 客户端存储token，并在每次请求时附送上这个token值
- 服务端验证token值，并返回数据

这个token必须要在每次请求时传递给服务端，它应该保存在请求头里， 另外，服务端要支持CORS(跨来源资源共享)策略，一般我们在服务端这么做就可以了Access-Control-Allow-Origin: *。

## JWT的构成  
第一部分为header，第二部分为payload，第三部分为signature  

**header**  
jwt的头部承载两部分信息：  
- 声明类型，这里是jwt
- 声明加密的算法 通常直接使用 HMAC SHA256
```
{
  'typ': 'JWT',
  'alg': 'HS256'
}
```
然后使用base64加密  

**payload**  
存放有效信息的地方，含有三个部分  
- 标准中注册的声明  
- 公共的声明  
- 私有的声明  

**标准中注册的声明**  
- iss
  jwt签发着  
- sub
  jwt所面向的用户
- aud  
  接收jwt的一方  
- exp
  jwt的过期时间
- nbf
  定义在什么时间之前，该jwt是不可用的
- iat
  jwt的签发时间
- jti
  jwt的唯一身份标识，主要用来作为一次性token,从而回避重放攻击。

**Signature**

jwt的第三部分是一个签证信息
- header base64
- payload base64
- secret
```
signature = HS256(base64(header).base64(payload), secret)
```
然后将三个字符串使用`.`相连接 ，就构成了jwt

请求头中加入Authorization