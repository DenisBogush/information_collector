# -*- coding: utf-8 -*-

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

SMTP_URL = 'smtp.gmail.com'
SMTP_PORT = 465


# функция отправки на почту сообщения с вложенным файлом
def send(subject, text, attachments, send_from, password, send_to):

    # Формируем вложение
    filename, bytes = attachments
    part = MIMEBase('application', "octet-stream")
    part.set_payload(bytes.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename={}'.format(filename))

    # Формируем сообщение
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.attach(part)
    msg.attach(MIMEText(text))

    # Отправляем почту
    smtp_url = SMTP_URL
    port = SMTP_PORT
    with SMTP_SSL(smtp_url) as smtp:
        smtp.connect(host=smtp_url, port=port)
        smtp.login(send_from, password)
        smtp.sendmail(send_from, send_to, msg.as_string())
