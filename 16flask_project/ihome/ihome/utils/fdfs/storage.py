# coding:utf-8
from fdfs_client.client import Fdfs_client

class FDFSStorage(object):
    '''fast dfs文件存储类'''
    def __init__(self, client_conf=None):
        '''初始化'''
        self.client_conf = client_conf

    def save_file(self, name, content):
        '''保存文件时使用'''
        # name:你选择上传文件的名字
        # content:包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)
        ext_file = name.split('.')[-1]
        # 上传文件到fast dfs系统中
        res = client.upload_by_buffer(content.read(),file_ext_name=ext_file)

        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename



