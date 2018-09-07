#coding:utf-8
from flask import Flask,render_template,request,flash,session,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Length

app = Flask(__name__)

app.config['SECRET_KEY'] = 'n+g1z1rh9i*rhalu_2cqc+m^n7^h@b+_m-4(mlunhh9872nm)p'

# 定义表单模型 类似django的form表单
class RegisterForm(FlaskForm):
    username = StringField(label=u'用&nbsp;户&nbsp;&nbsp;名:',validators=[DataRequired(u'用户不能为空'),
                                                                       Length(6,message=u'用户名长度不能低于6位')])
    password = PasswordField(label=u'密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码:',validators=[DataRequired(u'密码不能为空'),
                                                                                          Length(6,message=u'密码长度不能低于6位')])
    cpassword = PasswordField(label=u'确认密码:', validators=[DataRequired(u'密码不能为空'),
                                                          Length(6, message=u'密码长度不能低于6位'),EqualTo('password',u'两次输入的密码不一致')])
    submit = SubmitField(label=u'提交')

@app.route('/')
def index():
    username = session.get('username','')
    return 'Hello,%s' %username


@app.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = register_form.username.data
        passwd = register_form.password.data
        session['username'] = user
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            # flask闪现，信息只显示一次   {{ get_flashed_messages }}html接收flash消息
            flash('数据不完整，请重试！')

    return render_template('register.html',form=register_form)


if __name__ == '__main__':
    app.run(debug=True)