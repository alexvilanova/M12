import smtplib, ssl
from email.message import EmailMessage
from email.utils import formataddr
from urllib.parse import quote

class MailManager:

    def init_app(self, app):
        # agafo els paràmetres de configuració
        self.subject_prefix = app.config.get('MAIL_SUBJECT_PREFIX')
        self.sender_name = app.config.get('MAIL_SENDER_NAME')
        self.sender_addr = app.config.get('MAIL_SENDER_ADDR')
        self.sender_password = app.config.get('MAIL_SENDER_PASSWORD')
        self.smtp_server = app.config.get('MAIL_SMTP_SERVER')
        self.smtp_port = app.config.get('MAIL_SMTP_PORT')
        # URL del servidor per enviar tokens
        self.external_url = app.config.get('EXTERNAL_URL')

    def send_register_email(self, dst_name, dst_addr, token):
        subject = "Verifica el teu compte"
        content = f"""
Hola {dst_name},

Acabes de registrar-te a WannaPop. Per verificar el teu compte, fes clic al següent enllaç:

{self.external_url}/verify/{quote(dst_name)}/{quote(token)}

Si no has estat tu, ignora aquest correu.

Salutacions,

WannaPop
"""
        # s'envia l'email a l'usuari
        self.__send_mail(dst_name, dst_addr, subject, content)

    # https://realpython.com/python-send-email/#option-2-using-starttls
    def __send_mail(self, dst_name, dst_addr, subject, content):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(self.sender_addr, self.sender_password)

            print("Login done!")

            msg = EmailMessage()
            msg['From'] = formataddr((self.sender_name, self.sender_addr))
            msg['To'] = formataddr((dst_name, dst_addr))
            msg['Subject'] = self.subject_prefix + subject
            msg.set_content(content)

            server.send_message(msg, from_addr=self.sender_addr, to_addrs=dst_addr)
