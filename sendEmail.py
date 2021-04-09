import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_to_me(message, title):
    port = 465  # For SSL
    password = 'tlsBookDev'
    sender = 'tlsbookingdev@gmail.com'

    # TODO !! INSERT YOUR EMAIL(S)
    me = ['something at gmail.com', 'something else @ gmail.com']
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("tlsbookingdev@gmail.com", password)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = ', '.join(me)
        msg['Subject'] = title
        msg.attach(MIMEText(message))

        server.sendmail(sender, me, msg.as_string())
        server.quit()
