#!/usr/bin/env python
# -*- coding:utf-8 -*-


from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from smtplib import SMTP_SSL, SMTP


class Email:
    def __init__(self):
        pass

    def login_server(self, server, username, pwd, port=None, ssl=True):
        if port:
            self.smtp = SMTP_SSL(server, port=port) if ssl else SMTP(server, port=port)
        else:
            self.smtp = SMTP_SSL(server) if ssl else SMTP(server)
        self.smtp.login(username, pwd)

    def logout_server(self):
        self.smtp.quit()

    def __send_mail(self, from_addr, to_addrs, _subject, _content, _type=None):
        msg = None
        if _type:
            msg = MIMEText(_text=_content, _subtype=_type, _charset="utf-8")
        else:
            msg = MIMEText(_content)
        msg["From"] = from_addr
        msg["Subject"] = _subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid()
        self.smtp.sendmail(msg["From"], to_addrs, msg.as_string())

    def sendmail(self, from_addr, to_addrs, _subject, _content, content_type=None):
        self.__send_mail(from_addr, to_addrs, _subject, _content, content_type)

    def sendmail_batch(
        self,
        server,
        username,
        pwd,
        from_addr,
        to_addrs,
        _subject,
        _content,
        content_type=None,
    ):
        self.login_server(server, username, pwd)
        self.__send_mail(from_addr, to_addrs, _subject, _content, content_type)
        self.logout_server()


"""
Example 1:    mail_content = "<span>This is a auto-send mail.</span>"
    mail = Email("smtp.qq.com", "execute@qq.com", password, "send_user@qq.com", [
                  "recv1@qq.com", "recv2@qq.com"], "Test Moudle", mail_content, "html")
    mail.sendmail()
 Example 2:    mail_content = '
      Hi,
        This is a auto - send mail.'
    mail = Email("smtp.qq.com", "execute@qq.com", password, "send_user@qq.com", ["recv1@qq.com", "recv2@qq.com"],
    "Test Moudle", mail_content)
    mail.sendmail()
"""
