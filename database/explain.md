使用EXPLAIN对sql语句执行过程分析
```sql
MariaDB [samsdb]> EXPLAIN select * from hostmessage WHERE 服务码="12345678" AND 主机名="1111"\G;
*************************** 1. row ***************************
           id: 1
  select_type: SIMPLE
        table: hostmessage
         type: ref
possible_keys: ix_hostmessage_服务码,ix_hostmessage_主机名
          key: ix_hostmessage_服务码
      key_len: 303
          ref: const
         rows: 1
        Extra: Using index condition; Using where
```

各列的含义如下
- id SELECT 
  查询的标识符
- select_type SELECT  
  查询的类型
  - SIMPLE, 表示此查询不包含 UNION 查询或子查询
  - PRIMARY, 表示此查询是最外层的查询
  - UNION, 表示此查询是 UNION 的第二或随后的查询
  - DEPENDENT UNION, UNION 中的第二个或后面的查询语句, 取决于外面的查询
  - UNION RESULT, UNION 的结果
  - SUBQUERY, 子查询中的第一个 SELECT
  - DEPENDENT SUBQUERY: 子查询中的第一个 SELECT, 取决于外面的查询. 即子查询依赖于外层查询的结果
- table 查询的数据表
- type 查询涉及的表
  - system 
    表中只有一条数据. 这个类型是特殊的 const 类型
  - const 
    针对主键或唯一索引的等值查询扫描, 最多只返回一行数据. const 查询速度非常快, 因为它仅仅读取一次即可. 例如下面的这个查询, 它使用了主键索引, 因此 type 就是 const 类型的.
  - eq_ref
    此类型通常出现在多表的 join 查询, 表示对于前表的每一个结果, 都只能匹配到后表的一行结果
  - ref
    针对于非唯一或非主键索引, 或者是使用了 最左前缀 规则索引的查询
  - range
    表示使用索引范围查询,
  - index
    表示全索引扫描(full index scan), 和 ALL 类型类似, 只不过 ALL 类型是全表扫描, 而 index 类型则仅仅扫描所有的索引, 而不扫描数据.
  - ALL 
    全表扫描   

  执行效率  
  ALL < index < range ~ index_merge < ref < eq_ref < const < system
- possible_keys  
  表示 MySQL 在查询时, 能够使用到的索引
- key  
  此字段是 MySQL 在当前查询时所真正使用到的索引.
- key_len  
  表示查询优化器使用了索引的字节数.
- rows  
  rows 也是一个重要的字段. MySQL 查询优化器根据统计信息, 估算 SQL 要查找到结果集需要扫描读取的数据行数.
这个值非常直观显示 SQL 的效率好坏, 原则上 rows 越少越好
- Extra  
  额外的信息
  - using index
    查询时不需要回表查询，直接通过索引就可以获取查询的数据。
  - using filesort
    排序时无法使用到索引时，就会出现这个。常见于order by和group by语句中。
  - using where
    表示存储引擎返回的记录并不是所有的都满足查询条件，需要在server层进行过滤