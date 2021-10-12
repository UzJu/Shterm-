# -*- coding: UTF-8 -*-
'''
@Project ：SecurityTools 
@File    ：shterm_function.py
@IDE     ：PyCharm 
@Author  ：UzJu
@Date    ：2021/10/11 13:50 
@email   ：UzJuer@163.com
@GitHub  ：https://github.com/UzJu
// When I wrote this, only God and I understood what I was doing
// Now, God only knows
/*
* You may think you know what the following code does.
* But you dont. Trust me.
* Fiddle with it, and youll spend many a sleepless
* night cursing the moment you thought youd be clever
* enough to "optimize" the code below.
* Now close this file and go play with something else.
*/
'''
import requests
import json
import base64
import datetime
from requests_toolbelt import MultipartEncoder

requests.packages.urllib3.disable_warnings()


class shtermFunction:
    def __init__(self, Server_Url, ManagerID, ManagerPass):
        '''
        参数
            ManagerID: 接收管理员用户的ID
            ManagerPass：接收管理员用户的PasswordKey
        功能
            主要用途使用用来授权查询齐治堡垒机的接口
        '''
        self.ManagerID = ManagerID
        self.ManagerPass = ManagerPass
        self.Server_Url = Server_Url
        self.headers = {'identity': self.ManagerID, 'token': base64.b64decode(self.ManagerPass)}

    def verify_otp(self, user, otp):
        '''
        参数
            user 接收一个用户名
            otp 接收用户密码和双因素认证验证码
        功能
            认证用户是否合法
        '''
        url = F"{self.Server_Url}/api/identity/verify_passwd/byname/"
        datas = {"login": user, "password": otp}
        r = requests.get(url, headers=self.headers, params=datas, verify=False)
        return r.text

    def getShtermUserID(self, user):
        '''
        参数：user（用户名）
            使用用户名查询齐治堡垒机的ID
        功能
            获取指定用户的齐治堡垒机ID
        '''
        url = F"{self.Server_Url}/api/identity/query/?login={user}"
        r = requests.get(url, headers=self.headers, verify=False)
        return json.loads(r.text)['data'][0]['id']

    def update_Password_ExpireTime(self, id):
        '''
        参数
            id 接收用户ID
        功能
            更新用户密码有效期
        '''
        url = F'{self.Server_Url}/api/identity/passwd_expire/{id}/'
        expire_day = (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m-%d')
        datas = MultipartEncoder(fields={'date': expire_day})
        self.headers['Content-Type'] = datas.content_type
        r = requests.post(url, headers=self.headers, data=datas, verify=False)
        return r.text

    def update_Account_ExpireTime(self, id):
        '''
        参数
            id 接收用户ID
        功能
            更新用户账号有效期限
        '''
        url = F'{self.Server_Url}/api/identity/update/{id}/'
        expire_time = (datetime.date.today() + datetime.timedelta(days=90)).strftime('%Y-%m-%d') + " 23:59:00"
        datas = MultipartEncoder(fields={'valid_date2': expire_time})
        self.headers['Content-Type'] = datas.content_type
        r = requests.post(url, headers=self.headers, data=datas, verify=False)
        return r.text


# test = shtermFunction('https://172.29.0.206:8081', '42', 'QU9FY2hvaWNld2F5QDAyMjE=')
# verifyUser = test.verify_otp('Sec-Test', 'qwe@123')
# getUserId = test.getShtermUserID('Sec-Test')
# updatePassTime = test.update_Password_ExpireTime(getUserId)
# updateAccountTime = test.update_Account_ExpireTime(getUserId)
# print(verifyUser)
# print(getUserId)
# print(updatePassTime)
# print(updateAccountTime)