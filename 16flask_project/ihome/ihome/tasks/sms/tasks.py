#coding:utf-8
from ihome.tasks.main import app
from ihome.libs.sms.sms import CCP

@app.task
def send_sms(to, datas, tempId):
    """发送短信验证码"""
    ccp = CCP()
    ccp.sendTemplateSMS(to, datas, tempId)