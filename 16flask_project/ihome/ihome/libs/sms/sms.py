#coding:utf-8

from CCPRestSDK import REST
import ConfigParser

#主帐号
accountSid= '8a216da865e5a5f40165e61a4ab90045'

#主帐号Token
accountToken= 'e9e5e4895211474e899bf78408ef5b76'

#应用Id
appId='8a216da865e5a5f40165e61a4b14004b'

#请求地址，格式如下，不需要写http://
serverIP='app.cloopen.com'

#请求端口 
serverPort='8883'

#REST版本号
softVersion='2013-12-26'

  # 发送模板短信
  # @param to 手机号码
  # @param datas 内容数据 格式为列表 例如：[5674,3]，如不需替换请填 ''
  # @param $tempId 模板Id

class CCP(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        # 判断CCP类有没有创建好的对象，如果没有实列对象则创建对象并保存
        if cls.instance is None:
            obj = super(CCP, cls).__new__(cls)
            # 初始化REST对象
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)

            cls.instance = obj
        return cls.instance

    def sendTemplateSMS(self,to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        status = result.get('statusCode')
        if status == '000000':
            return 0
        else:
            return 1
        # for k, v in result.iteritems():
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)

        # smsMessageSid:160ef6e7c9784e80ad64346dff9bc1c4
        # dateCreated:20180917143747
        # statusCode:000000  #返回正确状态
