# Redis组件
redis-server

redis-cli

redis-benchmark

redis-check-dump & redis-check-aof
    RDB & AOF

>快照 save
    save 600 1 600s内一个键发生改变快照

`redis-cli`

        -h 帮助文件
        -p 服务器端口
        -s 指定本地socket文件
        -r 将指定命令执行n次
        -i 等待
        
Redis 键值存储

Keys
    ASCII
    尽量不要太长   
    
SELECT 1 多名称空间
    打开1号名称空间
    键名称不允许重复

# 数据结构
> 数据结构的操作方法
## String
* SET key value [NX|XX] [EX seconds]
* GET
* EXISTS
* INCR
* DECR

>SETNX
如果键不存在，则设置键
>SETXX
如果键存在，才设定键

## List
* RPUSH
* LPUSH
* LPOP
* RPOP
* LSET
* LINDEX
定义列表
LPUSH l1 mon
LINDEX l1 0
LSET l1 1 fri
## Set
* SADD
* SCARD
* SINTER 交集
* SUNION 并集
* SPOP
* SISMEMBER
## Sorted-Set
>help @sorted_set

* ZDD key store 
* ZSCORE 根据索引建立
* ZRANGE 起始索引 结束索引
* ZCARD 
* ZCOUNT 指定范围内

## Hash
* HSET
* HGET
* HGETALL
* HDEL
* HSCAN 遍历每一值
* HKEYS 
* HVALS 
* HSETNX
## Bitmaps, HyperLogLog


# 认证实现方法
    redis.conf
       requirepass password
       AUTH password

# 清空数据裤
    FLUSHDB  清空当前库
    FLUSHALL 清空所有库
# 事务
>通过MUTI，EXEC，WATCH等命令来实现事务功能。将一个或者多个命令归并为一个操作请求服务器按顺序执行的机制

    MUTI 启动一个事务
    EXEC 执行事务
        一次性将事务中的操作执行完成后返回给客户端
    WATCH 事务中相关联的键 在EXEC命令执行之前，用于监视指定数量键，如果监视中的某任意锁数据被修改，则服务器拒绝执行此事务
> 不支持回滚机制
    原子性
    隔离性
    一致性
    持久性 需开启

# Connection相关的命令
AUTH 密码
PING 测试服务器是否在线
ECHO 
SELECT 挑选指定的名称空间 

# Server 相关命令
ClIENT GETNAME
CLIENT KILL ip port 关闭对应client连接
CLIENT SETNAME name 设定连接NAME

INFO [ ]显示当前Redis服务器状态

CONFIG RESETSTAT 重置INFO统计的信息
CONFIG GET 获取配置参数
CONFIG SET 运行时修改指定配置
CONFIG REWRITE 将新的配置信息同步道配置文件中

DBSIZE 显示当前键的数量

BGSAVE
LASTSAVE
MONITOR
SHUTDOWN
SLAVEOF
SYNC
TIME

# 发布与订阅(publish/subscribe)

频道:消息队列

SUBSCRIBE:订阅一个或多个队列

SUBSCRIBE chanel

PSUBSCRIBE chanel_rex 模式订阅
> PSUBSCRIBE "news.i[to]"

PUBLISH chanel message

UNSUBSCRIBE chanel 


# Redis持久化
    RDB/AOF
        RDB：snapshot 二进制格式
            按事先定制的策略 周期性的将数据保存至磁盘，数据文件默认为dump.rdb
            客户端可以显示使用或者BGSAVE命令启动快照保存机制 
                SAVE：同步 在主线程中保存快照，此时会阻塞所有客户端请求
                BGSAVE：异步 不会被阻塞
            创建一个子进程 由子进程来实现创建快照功能
        AOF：Append Only File 将命令记录到文件尾部
            通过记录每一次写操作至指定的文件尾部实现持久化;当redis重启后，可通过重新执行文件中的命令在内存重建数据库;
            BGREWRITEAOF;
                不会读取正在使用的AOF文件，而通过将内存中的数据以命令的方式保存到临时文件中，完成之后替换原来的AOF文件
            缺点 文件会越来越大 
## RDB配置 
SAVE "" 关闭rdb
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb
dir /var/lib/redis

## AOF配置
    命令后将命令记录到文件
    重建过程
        1 redis 主进程通过fork创建子进程
        2 子进程根据redis内存中的数据创建数据库重建命令序列于临时文件
        3 父进程继承Vclient的请求，并会把这些请求中的写操作会继续追加至原来AOF文件 额外的 这些新的写请求还会继续被放置于一个缓冲队列中
        4 子进程重写完成 会同志父进程 父进程把缓冲中的命令写到临时文件中
        5 父进程用临时文件替换老的AOF文件

appendonly no 

appendfilename 

appendfsync always|everysec|no

        always 每次写操作度写到缓存文件中

        everysec 每秒中写一次  较好

        no 由操作系统决定何时写 
    
no-appendfsync-on-rewrite no 

        重写时对新的操作不做fsync

auto-aof-rewrite-percentage 100  


RDB AOF 同时使用

        1  当前aof文件大小是上BGREWRITE不会同时使用
        2  在Redis服务器启动时用于恢复数据时，会优先使用AOF 因为数据是最新的 

# Replication 复制
    特点：
        一个Master可以有多个Slave
        支持链式复制
        Master以非阻塞方式同步数据至slave
    过程：slave 发送请求同步主库数据 master会启动子进程 将数据快照保存在数据文件中，将数据文件发送给slave，slave收到数据文件保存到本地，然后重载至内存中 

        >SLAVEEOF ip port
        
        min-slaves-to-write 3
            从服务器少于3 禁止主服务器接受写请求
        min-slaves-max-log 10
            主从时间差不能大于10s

        注意：如果master使用requirepass开启了认证功能，从服务器要使用masterauth <PASSWORD> 来连入服务请求使用此密码进行认证

sentinel
    用于管理多个redis服务实现HA
            监控
            通知
            自动故障转移
            
    redis-sentinel /path/to/file.conf
    redis-server /path/to/file.cond --sentinel

    1 服务器自身初始化 运行redis-server 中专用与sentinel的功能的代码
    2 初始化sentinel状态，根据给定的配置文件，初始化监控的master服务器列表
    3 创建连向master的连接、

sentinel 配置文件

        (1) sentinel monitor <master_name> <ip> <redis_port> <quorum>
        eg: sentinel monitor myredis 127.0.0.1 26379 2

        (2) sentinel down-agter-milliseconds <master-name> <milliseconds>      主服务器下线最少经过的时常
        (3) sentinel parallel-syncs <master-name> <numslave>
                    设置多少从服务器可以同时像主服务器发起请求
        (4) sentinel fallower-timeout <master-name> <millisecond>
                    故障转移的超时时常
    专用命令：
            SENTINEL masters
            SENTINEL slave <mastr name>
            SENTINEL get-master-addr-by-name <master name>
            SENTINEL reset
            SENTINEL fallover <master name>
Clustering
        分布式数据库 通过分片机制进行数据分布。clustering内的    每个节点仅占数据库的一部分数据

        每个节点持有全局元数据 但仅持有一部分数据







# redis入门指南

## redis事务  
Redis中的事务(transaction)是一组命令的集合。事务同命令一样都是Redis的最小执行单元，一个事务中的命令要么都执行，要么都不执行。

使用`MUUTI`开始一个事务，然后把所有要在同一个事务中执行的命令都发送给 Redis后，我们使用EXEC命令告诉Redis将等待执行的事务队列中的所有命令(开始事务后，每一台输入命令都返回`QUEUED`的命令)按照发送顺序依次执行。命令在执行EXEC后才依次执行。  
Redis保证一个事务中的所有命令要么都执行要么都不执行。如果在发送`EXEC`命令前客户端短线，则Redis会清空事务队列，事务中的命令都不会执行。  
Redis事务保证在一个事务内的命令依次执行的过程中而不被其他命令插入

**错误处理**
- 语法错误  
在事务中只要有一个命令有`语法`错误，执行EXEC后Redis就会直接返回错误，正确的语法也不会执行。  
- 运行错误  
运行错误指在命令的执行是出现的错误。 如果事务里的一条命令出现了语法错误，事务里其他的命令依然会继续执行。

Redis的事务没有关系型数据库提供的回滚(rollback)功能

**WATCH监控命令**  
`WATCH`命令可以监控一个或者多个键，一旦其中有一个键被修改(或者被删除)之后的事务就不会被执行。监控一直EXEC执行前，也就是事务开始执行前。 所以在`MULTI`命令开始后可以修改WATCH监控的键值。  
基于此可以实现+1的原子操作  
```
WATCH $key
$value = GET $key
$value = $value + 1
MULTI 
set $key $value
EXEC
```
如果`EXEC`命令返回失败，则重新执行。

## 过期时间  
Redis中可以使用`EXPIRE`命令设置一个键的过期时间，到期后Redis回自动删除它。  
`set key seconds`

**Redis缓存的实现**  
使用制redis键值的过期时间来定期淘汰不用的key，可能会导致占满内存，另一方面太短，就可能导致缓存命中率太低并且大量内存闲置。  
可以限制redis能够使用的最大内存，并让Redis按照一定的规则淘汰不需要的缓存键，这种方式只讲Redis用作缓存键时非常有用。    
修改配置文件的`maxmemory`参数，限制Redis的最大可用内存(单位字节),当超出这个限制时Redis会根据`maxmemory-policy`参数指定的策略来删除不需要的键直到Redis占用的内存小于指定内存。  
`maxmemory-policy`支持的规则如表4-1所示。

规则 | 说明
---|---
volatile-lru | 使用`lru`算法删除一个键(只对设置了过期时间的键)
allkeys-lru | 使用`lru`算法删除一个键
volatile-random|随机删除一个键(只对设置过期时间的键)
allkeys-random|随机删除一个键
volatile-ttl|删除离过期时间最近的一个键
noeviction|不删除键，只返回错误

## 消息通知  
**任务队列**  
通知的过程可以使用任务队列来实现。与任务队列进行交互的实体有两类，一类是生产者(producer)，另一类是消费者(consumer)。生产者会将需要处理的任务放入任务队列中，而消费者则不断地从任务队列中读入任务信息并执行。  
任务队列的优点  
- 松耦合
生产者与消费者无需直到彼此的实现细节，只需要约定好的任务的描述格式。
- 易于扩展  
消费者可以有多个，而且可以分布在不同的服务器中。

要实现任务队列，只需要让生产者将任务使用`LPUSH`加入到某个键中，另一边让消费者不断地使用`RPOP`命令从该键中取出任务即可。  

使用`BRPOP`代替`RPOP`
`BRPOP`当列表中没有元素时，会一直阻塞，直到列表中有新元素加入。


# 持久化
Redis支持两种持久化方式，`RDB`和`AOF`

## RDB方式  
`RDB`方式的持久化是通过快照(snapshotting)完成的，当符合一定的条件时Redis会自动地将内存中所有数据生成一份副本并存储在硬盘上，这个过程即为快照。  
Redis会在以下情况下对数据进行快照：

* 根据配置规则进行自动快照

* 用户执行SAVE或BGSAVE   
    SAVE执行过程中会阻塞所有请求  
    BSGSAVE是在后台异步进行快照操作

* 执行FULLSHALL  
    清除数据库中的所有数据  
    当没有自定义自动快照条件时，执行FLASHALL则不会进行快照
* 执行复制(replication)时。


**快照过程**
1. Redis使用fork函数复制一份当前进程(父进程)的副本(子进程)  
2. 父进程继续接受并处理客户端发来的命令，而子进程开始将内存中的数据写入硬盘中的临时文件 
3. 当子进程写完所有的数据后用该临时文件替换旧的RDB文件。
>在进行复制时操作系统会使用写时复制策略(copy-on-write)， 即fork函数发生的一刻父子进程共享同一内存数据，当父进程要更改其中某片数据时，操作系统会将该片数据复制一份以保证子进程的数据不受影响，所以新的RDB文件存储的还是执行fork一刻的内存数据。

## AOF方式  
`AOF`是将Redis执行的每一条命令追加到硬盘文件中，这一过程会降低redis的性能

**开启AOF**  
```
appendonly yes                  # 开启aof
appendfilename appendonly.aof   # aof文件名
```
优化aof文件,自动将内存中不存在的键值去掉  
```
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```
数据大小为64mb后百分之百重写aof文件

**同步硬盘数据**  
由于操作系统的缓存机制，每次执行的命令并没有真正的写入硬盘，而是进入了系统的硬盘缓存。在默认情况下30s执行一次同步，以便将硬盘缓存写入硬盘。但可以设置以使每次都可以写入内存
```
# appendfsync always
appendfsync everysec
# appendfsync no
```
默认为每秒执行一次写入操作 `everysec`

# 集群
## 主从复制  
`redis-server --port 6380 --slaveof 127.0.0.1 6379`
**原理**  
当从服务器启动后，会向主服务器发送SYNC命令。同时主数据库接收到SYNC命令后开始在后台保存快照(RDB过程)，并将保存快照期间接收到的命令缓存起来。当完成快照后，Redis会将快照文件和所有缓存到的命令发送给从数据库。从数据库收到后载入快照文件然后执行收到的缓存命令。

Redis采用了乐观复制(optimistic replcation)的复制策略，容忍在一定时间内主从数据库是不同的，但是最终两者的数据会同步。

限制只有当数据同步给指定数量的从数据库时，主数据库才是采写的
```
max-slaves-to-write 3
max-slaves-max-log 10
```
最少3个从数据库连接，主数据库才是可写的
允许从数据库最长失去连接的时间为10s

## 哨兵
哨兵的作用就是监控Redis集群系统的运行情况。  
功能
- 监控主数据库和从数据库是否正常运行
- 主数据库出现故障时自动将从数据库转换为主数据库

是一个独立的进程。 
启动哨兵节点  
配置文件  
`rentinel monitor mymaster 127.0.0.1 6379 1`   
`1`为法定票数  
启动命令  
`redis-sentinel /etc/redis/sentinel.conf`

哨兵节点启动后会与要监控的主数据库建立两条连接，这两个连接的建立方式与普通Redis客户端相同。
一条连接用来订阅主数据的`__sentinel__:hello` 频道以获取`其他同样监控该数据库`的哨兵节点的信息，另外哨兵也需要定期地向主数据库发动`INFO`命令来获取主数据库本身的信息。  
和主数据库的连接建立完成后，哨兵会定期的执行下面3个操作。  
- 每10s哨兵向主数据库和从数据库发送`INFO`命令
- 每2s哨兵会向主数据库和从数据库的`__sentinel__:hello`频道发送自已的信息
- 每1s哨兵会向主从数据库和其他哨兵节点发送`PING`命令

`down-after-milliseconds 毫秒`值小于1s，哨兵会每隔这么多s发送一个`PING`命令，大于1s则每一秒发送`PING`命令

哨兵的法定票数`quorum`设置为`N/2+1`(N为哨兵节点数量)
