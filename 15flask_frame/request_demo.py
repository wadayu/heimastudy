# coding:utf-8

from flask import Flask,request

app = Flask(__name__)

@app.route('/register',methods=['GET','POST'])
def register():
    # reqeust.form 接收表单数据 dict类型
    username = request.form.get('username')
    age = request.form.get('age')
    gender = request.form.get('gender')
    # return 'Infomation: usernmae=%s,age=%s,gender=%s' % (username, age, gender)

    # request.data 接收表单以外的数据 POSTMAN RAW传来的json数据 string类型
    """
    data = eval(request.data)
    city = data.get('city')
    country = data.get('country')
    """
    # return 'Infomation: city=%s,country=%s' % (city,country)

    # http://127.0.0.1:5000/register?id=3&sort=hot （查询字符串）QueryString
    # reqeuest.args 接收url带来的的参数 dict类型
    id = request.args.get('id')
    sort = request.args.get('sort')
    # return 'Infomation: id=%s,sort=%s'  % (id,sort)

    # request.files 接收用户上传的文件 POSTMAT form-data方法
    file = request.files.get('pic')
    if file:
        file.save('./%s' %file.filename)
        return '上传成功'
    else:
        return '上传失败'


if __name__ == '__main__':
    app.run(debug=True)


















