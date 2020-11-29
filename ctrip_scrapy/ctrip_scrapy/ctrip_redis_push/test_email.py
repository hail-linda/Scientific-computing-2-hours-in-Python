from settings import EMAIL_SENDER, EMAIL_NAME, EMAIL_PWD
from qqmail import QQMail


qqm = QQMail(EMAIL_SENDER, EMAIL_PWD, EMAIL_NAME)

print(qqm.send(["jingle.mail@163.com", "123355370@qq.com"], "Hello", "Content"))