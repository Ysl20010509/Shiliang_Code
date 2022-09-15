import sendgrid
import os
from sendgrid.helpers.mail import *

def daily_report(report):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("shiliany@uci.edu")
    to_email = To("fei.xie@mentorx.net")
    to_email = To("shiliangyao509@gmail.com")
    subject = "Daily Report"
    content = Content("text/plain", report)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)