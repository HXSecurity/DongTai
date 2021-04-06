#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/3 上午9:16
# project: dongtai-webapi

import csv

from django.contrib.auth.models import Group

from base import R
from iast.base.user import TalentAdminEndPoint
from iast.models import User
from iast.models.department import Department
from iast.notify.email import Email
from webapi import settings


class UserRegisterEndPoint(TalentAdminEndPoint):

    def get(self, request):
        users = self.read_user_data()
        self.register(users)
        return R.success(msg='账号创建成功')

    def read_user_data(self):
        header = True
        users = list()
        try:
            # fixme 后续增加上传功能，上传用户csv后自动创建并发送通知
            with open('/tmp/user_register.csv', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if header:
                        header = False
                        continue
                    users.append((row[11].strip(), row[12].strip(), row[13].strip()))
        except:
            print(f'用户账号文件读取错误')
        return users

    def register(self, users):
        if users:
            email = Email()
            email.login_server(server=settings.EMAIL_SERVER,
                               username=settings.EMAIL_USER,
                               pwd=settings.EMAIL_PASSWORD,
                               ssl=settings.ENABLE_SSL)
            for user in users:
                _user = User.objects.filter(username=user[0]).first()
                if _user:
                    print(f'用户{user[0]}已存在')
                else:
                    # todo 创建账号
                    password = f'{user[0]}@123'
                    to_addr = user[1]
                    phone = user[2]
                    new_user = User.objects.create_user(username=user[0], password=password, email=to_addr, phone=phone)
                    department = Department.objects.filter(id=42).first()
                    department.users.add(new_user)
                    group, success = Group.objects.get_or_create(name='user')
                    group.user_set.add(new_user)
                    email.sendmail(
                        from_addr=settings.EMAIL_FROM_ADDR,
                        to_addrs=[to_addr, settings.ADMIN_EMAIL],
                        _subject='洞态IAST账号创建成功',
                        _content=f'洞态IAST账号创建成功，登陆地址：http://iast.huoxian.cn:8000/login，账号：{user[0]}，密码：{password}\n登陆之后，请马上修改默认密码，然后重新登陆使用'
                    )
            email.logout_server()

    def register_success(self):
        pass
