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
select gender,group_concat(name,' 年龄:',age)  from infomation where gender='remale' group by gender; # 统计的女性，并显示名字年龄

select * from infomation limit 2; # 限制查询的个数为2
# 当前页显示的起止编号=（页数-1）*每页显示的个数
select * from infomation limit 0,2; # 每页显示2个，第一页
select * from infomation limit 2,2; # 每页显示2个，第二页
select * from infomation limit 4,2; # 每页显示2个，第三页
select * from infomation limit 6,2; # 每页显示2个，第四页




















