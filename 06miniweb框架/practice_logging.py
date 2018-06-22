#coding:utf-8
__author__ = 'WangDy'
__date__ = '2018/6/21 11:14'

import logging

# 将日志输出到终端 和 日志文件

# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO) # Log等级总开关

# 第二步，创建一个handler，用于写入日志文件
logfile = './log.txt'
fh = logging.FileHandler(logfile,mode='a')
fh.setLevel(logging.DEBUG) # 输出到file的log等级开关

# 第三步，创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING) # 输出到console的log等级开关

# 第四步，定义handler的输出格式
formatter=logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

logging.debug('This is debug')
logging.info('This is info')
logging.warning('This is warning')
logging.error('This is error')
logging.critical('This is critical')



# logging.basicConfig(level=logging.INFO,
#                     # filename='./info.log',
#                     # filemode='a',
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
#
# logging.debug('This is debug')
# logging.info('This is info')
# logging.warning('This is warning')
# logging.error('This is error')
# logging.critical('This is critical')
