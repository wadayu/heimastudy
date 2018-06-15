select database(); # 查询当前所在的数据库
select version();  # 查询当前的版本
select now();      # 查询当前的时间

select s.name,s.age from infomation as s; # 别名查询
select distinct gender  from infomation;  #去重查询
INSERT INTO infomation values(0,'白骨精',101,'1900.01.01',165,1,null,0) # 插入数据
select * from infomation;   # 查询数据
DELETE from infomation WHERE id=10; # 删除指定的行数据
select * from infomation where age>30 and age<50;
select * from infomation where name like '许%';
select * from infomation where name like '___'; # 一个下划线的代表一个字符，匹配三个字的名字
select * from infomation where name rlike '^猪.*';  # rlike匹配正则
select * from infomation where name rlike '^猪.*戒$';  # rlike匹配正则
select * from infomation where age in (33,39,101); # 查询年龄在(33,39,101)
select * from infomation where age not in (33,39,101); # 查询年龄不在(33,39,101)
select * from infomation where age between 20 and 40; # 查询年龄的范围20~40之间 包括20，40
select * from infomation where (age between 80 and 110) and gender=1;
select * from infomation where (age between 80 and 110) and gender=1 order by age; # 以年龄的升序排列（默认升序asc）
select * from infomation where (age between 80 and 110) and gender=1 order by age desc; # 以年龄的降序排列

select count(*) from infomation where gender='male'; # 查询gender为male的个数
select max(age) from infomation; # 查找年龄最大的
select min(age) from infomation; # 查找年龄最小的
select max(high) from infomation where gender='male'; # 查询男性身高最高的
select sum(age) from infomation; # 查询年龄之和
select avg(age) from infomation; # 查询平均年龄
select sum(age)/count(*) from infomation; # 等同上面的一条语句
select round(sum(age)/count(*),2) from infomation; # 平均值取两位小数

select gender,count(*) from infomation group by gender; # 以gender分组，统计各分组的个数
select gender,max(age) from infomation group by gender; # 以gender分组，统计各分组的最大年龄值
select gender,group_concat(name) from infomation group by gender;   # 以gender分组，查询各分组的名字
select gender,count(*)  from infomation where gender='remale' group by gender;  # 统计女性的数量
select gender,group_concat(name,' 年龄:',age)  from infomation where gender='remale' group by gender; # 统计的女性，并显示名字、年龄

select * from infomation limit 2; # 限制查询的个数为2
# 当前页显示的起止编号=（页数-1）*每页显示的个数
select * from infomation limit 0,2; # 每页显示2个，第一页
select * from infomation limit 2,2; # 每页显示2个，第二页
select * from infomation limit 4,2; # 每页显示2个，第三页
select * from infomation limit 6,2; # 每页显示2个，第四页

#########内连接（inner join）#########
# 查询两个表关联的部分
mysql> select * from infomation as i inner join address as a  on i.address_id=a.id;
+----+-----------+-----+------------+--------+--------+------------+-----------+----+-----------+
| id | name      | age | birthday   | high   | gender | address_id | is_delete | id | province  |
+----+-----------+-----+------------+--------+--------+------------+-----------+----+-----------+
|  1 | daoyun    |  22 | 1992-01-28 | 180.88 | remale |          1 |           |  1 | 北京市    |
|  2 | 史今      |  39 | 1981-01-11 | 177.00 | male   |          2 |           |  2 | 天津市    |
|  3 | 许三多    |  32 | 1985-12-24 | 168.00 | male   |          1 |           |  1 | 北京市    |
|  5 | 唐僧      |  88 | 1900-11-23 | 172.00 | male   |          2 |           |  2 | 天津市    |
|  6 | 猪八戒    |  85 | 1910-12-02 | 165.00 | male   |          3 |           |  3 | 重庆市    |
|  7 | 孙悟空    |  87 | 1908-09-22 | 168.00 | male   |          4 |           |  4 | 上海市    |
|  8 | 沙僧      |  80 | 1909-03-30 | 162.00 | male   |          5 |           |  5 | 广东市    |
|  9 | 白骨精    | 101 | 1900-01-01 | 165.00 | remale |          6 |           |  6 | 深圳市    |
+----+-----------+-----+------------+--------+--------+------------+-----------+----+-----------+
# 查询两个表关联的部分指定的字段
mysql> select i.name,i.age,a.province from infomation as i inner join address as a  on i.address_id=a.id;
+-----------+-----+-----------+
| name      | age | province  |
+-----------+-----+-----------+
| daoyun    |  22 | 北京市    |
| 史今      |  39 | 天津市    |
| 许三多    |  32 | 北京市    |
| 唐僧      |  88 | 天津市    |
| 猪八戒    |  85 | 重庆市    |
| 孙悟空    |  87 | 上海市    |
| 沙僧      |  80 | 广东市    |
| 白骨精    | 101 | 深圳市    |
+-----------+-----+-----------+
# 根据相关的条件排序
mysql> select a.province,i.* from infomation as i inner join address as a on i.address_id=a.id order by a.province,i.id;
+-----------+----+-----------+-----+------------+--------+--------+------------+-----------+
| province  | id | name      | age | birthday   | high   | gender | address_id | is_delete |
+-----------+----+-----------+-----+------------+--------+--------+------------+-----------+
| 上海市    |  7 | 孙悟空    |  87 | 1908-09-22 | 168.00 | male   |          4 |           |
| 北京市    |  1 | daoyun    |  22 | 1992-01-28 | 180.88 | remale |          1 |           |
| 北京市    |  3 | 许三多    |  32 | 1985-12-24 | 168.00 | male   |          1 |           |
| 天津市    |  2 | 史今      |  39 | 1981-01-11 | 177.00 | male   |          2 |           |
| 天津市    |  5 | 唐僧      |  88 | 1900-11-23 | 172.00 | male   |          2 |           |
| 广东市    |  8 | 沙僧      |  80 | 1909-03-30 | 162.00 | male   |          5 |           |
| 深圳市    |  9 | 白骨精    | 101 | 1900-01-01 | 165.00 | remale |          6 |           |
| 重庆市    |  6 | 猪八戒    |  85 | 1910-12-02 | 165.00 | male   |          3 |           |
+-----------+----+-----------+-----+------------+--------+--------+------------+-----------+

#########左连接（left join）######### 意思就是把左边表的内容都拿出来对比，没有的就null表示。  右连接用的不多
mysql> select * from infomation as i left join address as a on i.address_id=a.id;
+----+-----------+-----+------------+--------+--------+------------+-----------+------+-----------+
| id | name      | age | birthday   | high   | gender | address_id | is_delete | id   | province  |
+----+-----------+-----+------------+--------+--------+------------+-----------+------+-----------+
|  1 | daoyun    |  22 | 1992-01-28 | 180.88 | remale |          1 |           |    1 | 北京市    |
|  2 | 史今      |  39 | 1981-01-11 | 177.00 | male   |          2 |           |    2 | 天津市    |
|  3 | 许三多    |  32 | 1985-12-24 | 168.00 | male   |          1 |           |    1 | 北京市    |
|  5 | 唐僧      |  88 | 1900-11-23 | 172.00 | male   |          2 |           |    2 | 天津市    |
|  6 | 猪八戒    |  85 | 1910-12-02 | 165.00 | male   |          3 |           |    3 | 重庆市    |
|  7 | 孙悟空    |  87 | 1908-09-22 | 168.00 | male   |          4 |           |    4 | 上海市    |
|  8 | 沙僧      |  80 | 1909-03-30 | 162.00 | male   |          5 |           |    5 | 广东市    |
|  9 | 白骨精    | 101 | 1900-01-01 | 165.00 | remale |          8 |           | NULL | NULL      |
+----+-----------+-----+------------+--------+--------+------------+-----------+------+-----------+
# having是从取出的结果再进行过滤，where是从原表过滤
mysql> select * from infomation as i left join address as a on i.address_id=a.id having a.id is null;
+----+-----------+-----+------------+--------+--------+------------+-----------+------+----------+
| id | name      | age | birthday   | high   | gender | address_id | is_delete | id   | province |
+----+-----------+-----+------------+--------+--------+------------+-----------+------+----------+
|  9 | 白骨精    | 101 | 1900-01-01 | 165.00 | remale |          8 |           | NULL | NULL     |
+----+-----------+-----+------------+--------+--------+------------+-----------+------+----------+

mysql> select a.province,group_concat(name),count(*) from infomation as i inner join address as a on i.address_id=a.id group by a.province;
+-----------+--------------------+----------+
| province  | group_concat(name) | count(*) |
+-----------+--------------------+----------+
| 上海市    | 孙悟空             |        1 |
| 北京市    | 许三多,daoyun      |        2 |
| 天津市    | 史今,唐僧          |        2 |
| 广东市    | 沙僧               |        1 |
| 重庆市    | 猪八戒             |        1 |
+-----------+--------------------+----------+

# 设置i.address_id对应外键的id
update infomation as i inner join address as a on i.address_id=a.name set i.address_id=a.id;
# 设置address_id引用外键
alter table infomation add foreign key(address_id) references address(id);
# 查询infomation表的name字段，并插入student表中
insert into student(name) select name  from infomation group by name;
# 查询infomation表的name字段，创建student表，并插入student表中
create table student(id int(11) not null primary key auto_increment,name varchar(30) not null) select name from infomation group by name;


















































