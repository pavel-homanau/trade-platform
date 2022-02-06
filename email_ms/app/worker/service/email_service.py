import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import loads

from kafka import KafkaConsumer


class SendEmailService:
    _mail_subject = 'Trading platform'
    _mail_from = os.environ.get('MAIL_FROM')

    def __init__(self):
        """Set consumer from kafka, email_server."""
        self._consumer = KafkaConsumer(
            os.environ.get("EMAIL_TOPIC"),
            bootstrap_servers=[os.environ.get("BOOTSTRAP_SERVER")],
            group_id='my-group',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

        self._connect_email()

    def _connect_email(self):
        """Set connection to email server, if no connection -
        raise error."""

        try:
            self._server = smtplib.SMTP_SSL(os.environ.get("MAIL_SERVER"),
                                            int(os.environ.get("MAIL_PORT")))
            self._server.login(os.environ.get("MAIL_USERNAME"),
                               os.environ.get("MAIL_PASSWORD"))
        except TimeoutError:
            raise "No connect to email service."

    def _send_email(self, recipients_dict: dict):
        """Get buyer and seller emails, item from dict
        and send email."""

        self._buy_msg = MIMEMultipart()
        self._buy_msg['Subject'] = self._mail_subject
        self._buy_msg['From'] = self._mail_from

        self._sell_msg = MIMEMultipart()
        self._sell_msg['Subject'] = self._mail_subject
        self._sell_msg['From'] = self._mail_from

        buy_mail_body = f"You bought a {recipients_dict.get('item')}."
        sell_mail_body = f"You sold a {recipients_dict.get('item')}."

        self._buy_msg.attach(MIMEText(buy_mail_body, 'plain'))
        self._server.sendmail(os.environ.get("MAIL_USERNAME"),
                              recipients_dict.get('buyer_email'),
                              self._buy_msg.as_string())

        self._sell_msg.attach(MIMEText(sell_mail_body, 'plain'))
        self._server.sendmail(os.environ.get("MAIL_USERNAME"),
                              recipients_dict.get('seller_email'),
                              self._sell_msg.as_string())

    def send_email_task(self):
        """Get messages from kafka consumer and send emails.
        Close kafka consumer, smtp server."""
        for msg in self._consumer:
            self._send_email(msg.value)
            print(msg.value)

        self._consumer.close()
        self._server.quit()
