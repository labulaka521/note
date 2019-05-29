## 创建数据库CREATE DATABASE
```
mysql> create database test;
Query OK, 1 row affected (0.09 sec)
```
## 创建表CREATE TABLE
```
mysql> CREATE TABLE IF NOT EXISTS runoob_tbl ( 
>runoob_id INT AUTO_INCREMENT, 
>ruboob_title VARCHAR(100) NOT NULL, 
>runoob_author VARCHAR(40) NOT NULL, 
>submission_date DATE, 
>PRIMARY KEY(runoob_id) )ENGINE=InnoDB DEFAULT CHARSET=utf8;
Query OK, 0 rows affected, 1 warning (0.06 sec)
```
## 插入数据INSERT
```
mysql> INSERT INTO runoob_tbl  (
>ruboob_title, runoob_author,
>submission_date) 
>VALUES (
>'学习Python',
>'runoob', 
>NOW()
>);
Query OK, 1 row affected, 1 warning (0.09 sec)
```
## 查询数据SELECT
```
mysql> select * from runoob_tbl;
+-----------+--------------+---------------+-----------------+
| runoob_id | ruboob_title | runoob_author | submission_date |
+-----------+--------------+---------------+-----------------+
|         1 | 学习Python   | runoob        | 2018-10-27      |
+-----------+--------------+---------------+-----------------+
1 row in set (0.00 sec)
```
## 修改数据  
```
mysql> UPDATE runoob_tbl SET runoob_title='学习 C++' WHERE runoob_id=3;
Query OK, 1 rows affected (0.01 sec)
 
mysql> SELECT * from runoob_tbl WHERE runoob_id=3;
+-----------+--------------+---------------+-----------------+
| runoob_id | runoob_title | runoob_author | submission_date |
+-----------+--------------+---------------+-----------------+
| 3         | 学习 C++   | RUNOOB.COM    | 2016-05-06      |
+-----------+--------------+---------------+-----------------+
1 rows in set (0.01 sec)
```
## 修改表中字段ALTER
- 修改表名  
```
mysql> ALTER TABLE runoob_tbl CHANGE ruboob_title runoob_title VARCHAR(100);
Query OK, 0 rows affected (0.19 sec)
Records: 0  Duplicates: 0  Warnings: 0
```
- 删除字段  
`mysql> ALTER TABLE testalter_tbl  DROP i;`  
- 添加字段  
`mysql> ALTER TABLE testalter_tbl ADD i INT;`  
如果你需要指定新增字段的位置，可以使用MySQL提供的关键字 FIRST (设定位第一列)， AFTER 字段名（设定位于某个字段之后）。

- 修改字段的类型及名称  
`mysql> ALTER TABLE testalter_tbl MODIFY c CHAR(10);`  
`mysql> ALTER TABLE testalter_tbl CHANGE i j BIGINT;`  
- 修改字段默认值  
`ALTER TABLE testalter_tbl ALTER i SET DEFAULT 1000;`  
- 修改表名  
`mysql> ALTER TABLE testalter_tbl RENAME TO alter_tbl;`


## 查看表的结构DESC
```
mysql> desc runoob_tbl;
+-----------------+--------------+------+-----+---------+----------------+
| Field           | Type         | Null | Key | Default | Extra          |
+-----------------+--------------+------+-----+---------+----------------+
| runoob_id       | int(11)      | NO   | PRI | NULL    | auto_increment |
| runoob_title    | varchar(100) | YES  |     | NULL    |                |
| runoob_author   | varchar(40)  | NO   |     | NULL    |                |
| submission_date | date         | YES  |     | NULL    |                |
+-----------------+--------------+------+-----+---------+----------------+
```
## 组合到一个结果集合中 UNION   
>MySQL UNION 操作符用于连接两个以上的 SELECT 语句的结果组合到一个结果集合中。多个 SELECT 语句会删除重复的数据。

```
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
```
- expression1, expression2  要检索的列  
- table 检索的表  
- where conditions 检索条件
- DISTINCT 删除集合中重复的元素
- ALL 返回所有的结果集

## Mysql结果排序  
`ORDER BY submission_date ASC;`

`ASC`顺序排序  
`DESC`逆序排序

## 连接查询  join
- INNER JOIN(内连接)  
获取两个表中字段匹配的记录  
- LEFT JOIN(左连接)  
获取左表所有记录，右表没有对应记录则使用NULL表示  
- RIGHT JOIN(右连接)  
获取左表所有记录，右表没有对应记录则使用NULL表示


**INNER JOIN**  
使用MySQL的INNER JOIN(也可以省略 INNER 使用 JOIN，效果一样)来连接以上两张表来读取runoob_tbl表中所有runoob_author字段在tcount_tbl表对应的runoob_count字段值：
```
mysql> select a.runoob_id, a.runoob_author, b.runoob_count 
>from runoob_tbl a 
>INNER JOIN tcount_tbl b 
>ON a.runoob_author = b.runoob_author;
+-----------+---------------+--------------+
| runoob_id | runoob_author | runoob_count |
+-----------+---------------+--------------+
|         1 | 菜鸟教程      |           10 |
|         2 | 菜鸟教程      |           10 |
|         3 | RUNOOB.COM    |           20 |
|         4 | RUNOOB.COM    |           20 |
+-----------+---------------+--------------+
4 rows in set (0.00 sec)
```
使用`WHERE`子句
```
mysql> select a.runoob_id, a.runoob_author, b.runoob_count 
>from runoob_tbl a,tcount_tbl b 
>WHERE a.runoob_author = b.runoob_author;
+-----------+---------------+--------------+
| runoob_id | runoob_author | runoob_count |
+-----------+---------------+--------------+
|         1 | 菜鸟教程      |           10 |
|         2 | 菜鸟教程      |           10 |
|         3 | RUNOOB.COM    |           20 |
|         4 | RUNOOB.COM    |           20 |
+-----------+---------------+--------------+
4 rows in set (0.00 sec)
```
![](http://ww1.sinaimg.cn/large/005Oh4GZly1fwmt816404g305k041mx2.jpg)

**LEFT JOIN**  
左连接会读取左表的数据，然后检索对应右表的数据，不存在则为NULL
```
mysql> select a.runoob_id,a.runoob_author, b.runoob_count 
>FROM runoob_tbl a 
>LEFT JOIN tcount_tbl b 
>ON a.runoob_author = b.runoob_author;
+-----------+---------------+--------------+
| runoob_id | runoob_author | runoob_count |
+-----------+---------------+--------------+
|         1 | 菜鸟教程      |           10 |
|         2 | 菜鸟教程      |           10 |
|         3 | RUNOOB.COM    |           20 |
|         4 | RUNOOB.COM    |           20 |
|         5 | FK            |         NULL |
+-----------+---------------+--------------+
5 rows in set (0.00 sec)
```
![](http://ww1.sinaimg.cn/large/005Oh4GZly1fwmui7lsnlg305k0413yf.jpg)  

**RIGHT JOIN**

读取右边数据表的全部数据
```
mysql> select a.runoob_id,a.runoob_author, b.runoob_count FROM runoob_tbl a RIGHT JOIN tcount_tbl b ON a.runoob_author = b.runoob_author;
+-----------+---------------+--------------+
| runoob_id | runoob_author | runoob_count |
+-----------+---------------+--------------+
|         1 | 菜鸟教程      |           10 |
|         2 | 菜鸟教程      |           10 |
|         3 | RUNOOB.COM    |           20 |
|         4 | RUNOOB.COM    |           20 |
|      NULL | NULL          |           22 |
+-----------+---------------+--------------+
5 rows in set (0.00 sec)
```
![](http://ww1.sinaimg.cn/large/005Oh4GZly1fwmw2mbv35g305k041a9z.jpg)

## Mysql排序  

- 在Mysql中只有使用InnoDb数据库引擎的数据库或表才可以支持事物
- 事物可以维护数据库的完整性，保证成批的SQL语句要么全部执行要么全部不执行  
- 事务是来管理insert，update，delete语句

**ACID**
- 原子性(atomicity)  
一个事务(transation)中的所有操作，要么全部不执行，要么全部执行。事务在执行过程中发生错误，会被回滚(rollback)到事务开始前的状态。  
- 一致性(consistency)   
在事务开始之前和事务结束以后，数据库的完整性没有被破坏。
- 隔离性(isolation)  
数据库允许多个并发事务对其数据进行读写和修改的能力。隔离型可以防止多个事务并发执行时由于交叉而导致数据不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。  
- 独立性(durability)  
事务处理结束之后，对数据的修改时永久的。  

**事务控制语句：**    

- BEGIN或START TRANSACTION  
显式地开启一个事务  

- COMMIT  
也可以使用COMMIT WORK，不过二者是等价的。COMMIT会提交事务，并使已对数据库进行的所有修改成为永久性的； 

- ROLLBACK有可以使用ROLLBACK  WORK  
不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改

- SAVEPOINT identifier  
SAVEPOINT允许在事务中创建一个保存点，一个事务中可以有多个SAVEPOINT  

- RELEASE SAVEPOINT identifier  
 删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常  

- ROLLBACK TO identifier  
把事务回滚到标记点  

- SET TRANSACTION   
用来设置事务的隔离级别。InnoDB存储引擎提供事务的隔离级别有READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ和SERIALIZABLE。



**MYSQL 事务处理主要有两种方法：**
- 用 BEGIN, ROLLBACK, COMMIT来实现  
BEGIN 开始一个事务   
ROLLBACK 事务回滚  
COMMIT 事务确认  
- 直接用 SET 来改变 MySQL 的自动提交模式:  
SET AUTOCOMMIT=0 禁止自动提交  
SET AUTOCOMMIT=1 开启自动提交


```
mysql> CREATE TABLE transation(id int) ENGINE=InnoDb;
Query OK, 0 rows affected (0.11 sec)

mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> insert into transation value(1);
Query OK, 1 row affected (0.02 sec)

mysql> insert into transation value(2);
Query OK, 1 row affected (0.00 sec)

mysql> commit;
Query OK, 0 rows affected (0.07 sec)

mysql> select * from transation;
+------+
| id   |
+------+
|    1 |
|    2 |
+------+
2 rows in set (0.01 sec)

mysql> begin;
Query OK, 0 rows affected (0.00 sec)

mysql> insert into transation value(3);
Query OK, 1 row affected (0.00 sec)

mysql> insert into transation value(4);
Query OK, 1 row affected (0.00 sec)

mysql> select * from transation;
+------+
| id   |
+------+
|    1 |
|    2 |
|    3 |
|    4 |
+------+
4 rows in set (0.00 sec)

mysql> rollback;
Query OK, 0 rows affected (0.05 sec)

mysql> select * from transation;
+------+
| id   |
+------+
|    1 |
|    2 |
+------+
2 rows in set (0.00 sec)
```

## MySQL 索引
索引分单列索引和组合索引。单列索引，即一个索引只包含单个列，一个表可以有多个单列索引，但这不是组合索引。组合索引，即一个索引包含多个列。  
虽然索引大大提高了查询速度，同时却会降低更新表的速度，如对表进行INSERT、UPDATE和DELETE。因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件。  

**普通索引**  
-  创建索引  
`CREATE INDEX indexName ON mytable(username(length)); `
- 修改表结构 添加索引  
`ALTER table tablename ADD INDEX indexname(columName);`  
- 创建表时加入索引  
```
CREATE TABLE tablename(  
ID INT NOT NULL,  
username VARCHAR(16) NOT NULL,  
INDEX [indexname] (username)  
);
```
- 删除索引  
`delete index [indexname] on tablename;`

**唯一索引**  
与普通索引类似，不同的是索引的值必须唯一但允许有空值。如果是组合索引，则列值的组合必须唯一。  
- 创建索引    
`CREATE UNIQUE INDEX indexName ON mytable(username(length)) `  
- 修改表结构  
`ALTER table mytable ADD UNIQUE [indexName] (username(length))`
- 创建表时添加  
```
CREATE TABLE mytable(  
ID INT NOT NULL,   
username VARCHAR(16) NOT NULL, 
UNIQUE [indexName] (username(length))  
);  
```
查看表结构  
```
> show create table runoob_tbl\G;
*************************** 1. row ***************************
       Table: runoob_tbl
Create Table: CREATE TABLE `runoob_tbl` (
  `runoob_id` int(11) NOT NULL AUTO_INCREMENT,
  `runoob_title` varchar(100) NOT NULL,
  `runoob_author` varchar(40) NOT NULL,
  `submission_date` date DEFAULT NULL,
  PRIMARY KEY (`runoob_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8
1 row in set (0.00 sec)
```


unique 和 primark key的区别

`unique key` 是唯一键 可以在多个列存在，设置unique的列可以为空null，不能包含重复的值 ，
`primark key` 是主键 只可以存在一个列，并且不可以为空，
