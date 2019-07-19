# opentracing数据模型
Opentracing中的Trace(调用链)通过归属于此调用链来隐性的定义  
一条Trace可以被认为是由多个Span组成的有向无环图(DAG),Span与Span的 关系被命名为References

Trace
```
单个Trace中，span间的时间关系


––|–––––––|–––––––|–––––––|–––––––|–––––––|–––––––|–––––––|–> time

 [Span A···················································]
   [Span B··············································]
      [Span D··········································]
    [Span C········································]
         [Span E·······]        [Span F··] [Span G··] [Span H··]
```

每个Span包括以下的状态
- An operation name，操作名称
- A start timestamp，起始时间
- A finish timestamp，结束时间
- Span Tag，一组键值对构成的Span标签集合。键值对中，键必须为string，值可以是字符串，布尔，或者数字类型。
- Span Log，一组span的日志集合。 每次log操作包含一个键值对，以及一个时间戳。 键值对中，键必须为string，值可以是任意类型。 但是需要注意，不是所有的支持OpenTracing的Tracer,都需要支持所有的值类型。
- SpanContext，Span上下文对象 (下面会详细说明)
- References(Span间关系)，相关的零个或者多个Span（Span间通过SpanContext建立这种关系）

每个SpanContext包含以下状态
- 任何一个OpenTracing的实现，都需要将当前调用链的状态，依赖一个独特的Span去跨进程边界传输
- Baggage Items： Trace的随行数据，是一个键值对集合，它存在于trace中，也需要跨进程边界传输

## Span间关系
一个Span可以与一个后者多个SpanContexts存在因果关系。Opentracing目前定义了两种关系：ChildOf(父子)和FollowsFrom(跟随)。

- ChildOf引用
  一个span可能是一个父级span的孩子，父级span某种程度依赖子span
  - 
- FollowsFrom引用
  一个父级节点不以任何方式依赖他们子节点的执行结果