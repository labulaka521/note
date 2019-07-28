`Protobuf`是一种轻便高效的结构化数据存储格式，可以用于结构化数据序列化，很适合做数据存储或RPC数据交换协议。它可以用户通讯协议，数据存储等领域的语言无关平台无关可扩展的序列化结构数据格式，pb属于二进制格式，传输速度快，更容易解析
 
# Protobuf 消息定义的规则

## 定义
```proto
message SearchRequest {
  required string query = 1;
  optional int32 page_number = 2;
  optional int32 result_per_page = 3;
}
```

proto文件的消息定义每一个字段都有唯一的`数字标识符`。这些标识符是用来在消息的二进制格式中识别各个字段的，一旦使用就不能在更改  
1-15之内的表示好在编码的时候会占用一个字节 16-2047之内的标识符则占用两个字节。


## 字段规则  

- required: 表示该值是必须要设置的
- optional: 消息格式中改革字段可以有0个或者1个
- repeated: 字段可以重复人意多次
  repeated字段没有被尽可能的搞笑编码。可以加[package=true]来保证更高效的编码
  ```
  repeated int32 samples = 4 [packed=true];
  ```

optional的字段默认值
```
optional int32 result_per_page = 3 [default = 10];
```
当没有为optional的元素指定默认值，就会使用后面定义的默认值  
```
string -> ""  
bool -> false  
int -> 0 
``` 

## 枚举
为消息定义指定为预定义的值中的一个

```
message Search {
    enum Corpus {
        UNIVERSAL = 0;
        WEB = 1;
        IMAGES = 2;
        LOCAL = 3
    }
    optional Corpus corpus = 1; [default = UNIVERSAL]
}
```

## 定义消息类型为其他的消息定义

当`SearchResponse`消息中包含`Result`消息，此时可以在相同的.proto文件中定一个`Result`类型,然后在`SearchResponse`消息中指定一个`Result`类型的字段
```
message SearchResponse {
  repeated Result result = 1;
}
message Result {
  required string url = 1;
  optional string title = 2;
  repeated string snippets = 3;
}
```

## OneOf

如果消息中有很多可选字段，并且同时之多一个字段会被设置，那么可以使用oneof,但是不可以使用required, optional, repeated 关键字.

```
message SampleMessage {
    oneof test_oneof {
        string name = 4;
        SubMessage sub_message = 9;
    }
}
```
特性 
- 设置oneof自动自动清楚其他oneof字段的值，
- 不能使用repeated

## 包
为proto文件新增一个可选的package声明符，用来防止不同的消息类型有命名冲突。

```
package foo.bar;
message Open { 

}


message Foo {
  ...
  required foo.bar.Open open = 1;
  ...
}
```