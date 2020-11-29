import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from log import get_logger


class QQMail:
    sender = ''
    pwd = ''
    sender_name = ""
    logger = get_logger()

    def __init__(self, sender, pwd, sender_name=""):
        self.sender = sender
        self.pwd = pwd
        self.sender_name = sender_name

    def send(self, recipients, subject, content=""):
        ret = True
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['From'] = formataddr([self.sender_name, self.sender])
            msg['To'] = ", ".join(recipients)


            msg['Subject'] = subject

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(self.sender, self.pwd)
            server.sendmail(self.sender, recipients, msg.as_string())
            server.quit()
        except Exception as e:
            self.logger.exception(e)
            ret = False
        return ret


