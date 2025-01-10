from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

from .handle import NotificationHandle

class EmailNotificationHandle(NotificationHandle):
    def __init__(self,fromEmail:str,toEmail:str,emailPassword:str,hostAddress:str='') -> None:
        super().__init__()
        self.__fromEmail = fromEmail
        self.__toEmail = toEmail.split("|")
        self.__emailPassword = emailPassword
        self.__hostAddress = hostAddress or "smtp."+fromEmail.split("@")[1]
        if ':' in self.__hostAddress:
            [addr, port] = self.__hostAddress.split(':')
            self.__hostAddress = addr
            self.__hostPort = int(port)
        else:
            self.__hostPort = 0

    def send(self,result):
        
        # {'success': True, 'visa_type': 'NONIMMIGRANT VISA APPLICATION', 'status': 'Issued', 'case_created': '30-Aug-2022', 'case_last_updated': '19-Oct-2022', 'description': 'Your visa is in final processing. If you have not received it in more than 10 working days, please see the webpage for contact information of the embassy or consulate where you submitted your application.', 'application_num': '***'}

        mail_title = '美签状态监控: {}'.format(result['status'])

        # 格式化邮件内容为 HTML 格式，使用 <br> 标签换行
        mail_content_html = (
            f"<html><body>"
            f"<p><strong>Time:</strong> {result['time']}</p>"
            f"<p><strong>Visa Type:</strong> {result['visa_type']}</p>"
            f"<p><strong>Status:</strong> <span style='color:red; font-weight:bold;'>{result['status']}</span></p>"
            f"<p><strong>Case Created:</strong> {result['case_created']}</p>"
            f"<p><strong>Case Last Updated:</strong> {result['case_last_updated']}</p>"
            f"<p><strong>Description:</strong> {result['description']}</p>"
            f"<p><strong>Application Number:</strong> {result['application_num']}</p>"
            f"<p><strong>Original Application Number:</strong> {result['application_num_origin']}</p>"
            f"<p>--- End of Status Update ---</p>"
            f"</body></html>"
        )

        msg = MIMEMultipart()
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = self.__fromEmail
        msg['To'] = ";".join(self.__toEmail)
        msg.attach(MIMEText(mail_content_html, 'html', 'utf-8'))

        smtp = SMTP_SSL(self.__hostAddress, self.__hostPort)  # ssl登录
        print(smtp.login(self.__fromEmail, self.__emailPassword))
        print(smtp.sendmail(self.__fromEmail, self.__toEmail, msg.as_string()))
        smtp.quit()
