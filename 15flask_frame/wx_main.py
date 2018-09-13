#coding:utf-8
from flask import Flask,request,abort

import pymysql
pymysql.install_as_MySQLdb()

import hashlib,xmltodict,time,urllib


AppID = 'wx69e06bb0d3d1e137'
AppSecret = 'f081fe911f02dbf0e6445de3c5a8f5ab'

app = Flask(__name__)
# 获取access_token
# res = urllib.urlopen("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" %(AppID,AppSecret))
# res = eval(res.read())
#
# if 'errcode' in res:
#     print ('请求错误')
# access_token = res.get('access_token')

# class Menu(object):
#     def __init__(self):
#         pass
#
#     def create(self, postData, accessToken):
#         postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
#         postData = postData.encode('utf-8')
#         urlResp = urllib.urlopen(url=postUrl, data=postData)
#         print (urlResp.read())


@app.route('/wechat',methods=['POST','GET'])
def index():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')

    token = "wadayu"  # 请按照公众平台官网\基本配置中信息填写

    if not all([signature,timestamp,nonce]):
        abort (400)

    li = [token, timestamp, nonce]
    li.sort()
    str = ''.join(li)
    signa =  hashlib.sha1(str.encode('utf8')).hexdigest()

    if signa != signature:
        abort(403)
    else:
        if request.method == 'GET':
            echostr = request.args.get('echostr')
            if not echostr:
                abort(400)
            return echostr
        elif request.method == 'POST':
            xml_data = request.data
            # 将xml格式转换成dict
            dict_data = xmltodict.parse(xml_data).get('xml')

            if dict_data.get('MsgType') == 'text':
                send_msg = {'xml':{
                    'ToUserName':dict_data.get('FromUserName'),
                    'FromUserName':dict_data.get('ToUserName'),
                    'CreateTime':int(time.time()),
                    'Content':dict_data.get('Content'),
                    'MsgType':'text'
                }}
            elif dict_data.get('MsgType') == 'event':
                if dict_data.get('Event') == 'subscribe':
                    send_msg = {'xml': {
                        'ToUserName': dict_data.get('FromUserName'),
                        'FromUserName': dict_data.get('ToUserName'),
                        'CreateTime': int(time.time()),
                        'Content': '欢迎关注运维文档',
                        'MsgType': 'text'
                    }}

                else:
                    return  ''

            else:
                send_msg = {'xml': {
                    'ToUserName':dict_data.get('FromUserName'),
                    'FromUserName':dict_data.get('ToUserName'),
                    'CreateTime':int(time.time()),
                    'Content':'嘻嘻',
                    'MsgType': 'text'
                }}

            return xmltodict.unparse(send_msg)

if __name__ == '__main__':
    # myMenu = Menu()
    # postJson = """
    #     {
    #         "button":
    #         [
    #             {
    #                 "type": "click",
    #                 "name": "开发指引",
    #                 "key":  "mpGuide"
    #             },
    #             {
    #                 "name": "公众平台",
    #                 "sub_button":
    #                 [
    #                     {
    #                         "type": "view",
    #                         "name": "更新公告",
    #                         "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
    #                     },
    #                     {
    #                         "type": "view",
    #                         "name": "接口权限说明",
    #                         "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
    #                     },
    #                     {
    #                         "type": "view",
    #                         "name": "返回码说明",
    #                         "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
    #                     }
    #                 ]
    #             },
    #             {
    #                 "type": "media_id",
    #                 "name": "旅行",
    #                 "media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
    #             }
    #           ]
    #     }
    #     """
    # myMenu.create(postJson, access_token)
    app.run(debug=True)