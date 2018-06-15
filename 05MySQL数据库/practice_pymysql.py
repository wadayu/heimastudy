#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/15 10:35'

from pymysql import connect


class InforMation(object):

    def __init__(self):
        # 连接数据库
        self.conn = connect(host='192.168.1.155', port=3306, user='windown', password='666666', db='jingdong', charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        # 关闭连接
        self.cursor.close()
        self.conn.close()

    def execute_sql(self,sql):
        self.cursor.execute(sql)
        for name in self.cursor.fetchall():
            print (name)

    def show_all_students(self):
        sql = 'select name from infomation'
        self.execute_sql(sql)

    def show_all_province(self):
        sql = 'select province from address'
        self.execute_sql(sql)

    def get_info_student(self):
        s_name = input('请输入想要查询的学生: ')
        sql = "select * from infomation where name=%s"
        # 防止SQL注入，将获取的变量放入列表，sql语句里有几个%s 列表里就需要有几个值
        res = self.cursor.execute(sql,[s_name])
        print (self.cursor.fetchall()) if res else print ('没有找到相关信息')

    def add_province(self):
        p = input('请输入你要添加的省份: ')
        sql = "insert into address(province) values('%s');" % p
        self.cursor.execute(sql)
        self.conn.commit()

    @staticmethod
    def print_num():
         # 打印想要查询的分类
        print ('1、查询所有的学生姓名')
        print ('2、查询所有的学生的省份')
        print ('3、添加一个省份')
        print ('4、查询学生的信息')
        return input('请输入你要查询的编号： ')

    def run(self):
        while True:
            num = self.print_num()
            # 获取分类，并运行对应的方法
            if num == '1':
                # 查询所有的学生姓名
                self.show_all_students()
            elif num == '2':
                # 查询所有的学生的省份
                self.show_all_province()
            elif num == '3':
                # 添加一个省份
                self.add_province()
            elif num == '4':
                # 查询某个学生的相关信息
                self.get_info_student()
            else:
                print ('输入的编号不正确')
                break

def main():
    # 创建一个实类对象
    info = InforMation()
    # 运行实类对象的方法
    info.run()

if __name__ == '__main__':
    main()

