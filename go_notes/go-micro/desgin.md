# Go Micro

![](../../image/go-micro.svg)

## Registry 注册模块
Registry注册模块提供可插拔的服务注册和发现功能

## Selector
Selector 选择器通过选举提供负载均衡机制。当客户端请求服务时，它首先要向查询到服务注册，一般情况是返回所需服务的注册成功的节点列表。选择器会选择其中一个用来提供服务。多次调用会触发均衡算法，当前的算法有轮询，哈希随机，黑名单。

## Broker
事件广播/订阅的可插拔接口，对于事件驱动的微服务架构，消息广播与订阅得放在首要位置。目前的实现有NATs、rabbitmq、http。

## Transport
可插拔的点对点消息传输接口，通过提供这种抽象，可以无缝地进行交换传输。目前的实现有http，rabbitmq，nats。

## Client
Client客户端提供发起RPC请求的能力。它集合了注册（registry）、选择器（selector）、broker、传输（transport），当然也具备重试、超时、上下文等等

## Server
Server服务就是运行了真实的微服务的程序，它提供的服务通过RPC请求的完成。