from .utils import uniqid_email
from . import mail, Message


class Email:

    def __init__(self, names, username, email):
        self.names = names
        self.username = username
        self.logo = "https://getsave.io/img/save_logo.png"
        self.email = email
        self.key = uniqid_email()
        self.login = "http://localhost:3000/#/signin"
        self.recover = "http://localhost:3000/#/recover/{email}/{random}".format(email=email, random=self.key)
        self.footer = "For any inquiry e-mail us on info@getsave.io or call us on " \
                      "+250 785-489-992<p>Thanks for using Save, enjoy." \
                      "<br>Save Team"

    def account(self):

        msg = Message('Account creation', sender='Save Team', recipients=[self.email])
        content = '<div style=padding-left:20px;width:100%;background-color:#fff>' \
                  '<div style=margin-left:0;padding-top:50px;padding-bottom:20px>' \
                  '<img src={logo} style=margin-left:-10px;margin-top:20px;height:40px>' \
                  '<p style=font-family:sans-serif;margin-left:0;padding-top:15px;color:#424242>' \
                  'Hallo <span style=font-weight:700>{names},</span>' \
                  '<p style=font-family:sans-serif;margin-left:0;color:#424242>' \
                  'Welcome to Save<p style=font-family:sans-serif;margin-left:0;color:#424242>' \
                  '- Your Username: {username}<br>- Sign in here to change password : {link}' \
                  '<p style=font-family:sans-serif;margin-left:0;color:#424242>{footer}</div></div>' \
                  '<div style=padding-left:20px;width:100%;padding-top:5px;background-color:#FAFAFA>' \
                  '<div style=margin-left:0px;margin-top:10px;margin-bottom:10px;>' \
                  '<span style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>' \
                  'You\'re receiving this message because you are a Save user send us feedback on ' \
                  'info@getsave.io or call us +250785489992</span>' \
                  '<p style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>' \
                  'Save is a product of <a href=http://www.exuus.com target=_blank>exuus Ltd.</a>' \
                  '<br>Exuus is a limited corporation registered in Republic of Rwanda.</p></div></div>'\
            .format(names=self.names, username=self.username, link=self.recover, footer=self.footer, logo=self.logo)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)
        return True

    def reset_link(self):

        msg = Message('Password reset link', sender='Save Team', recipients=[self.email])
        content = "<div style=padding-left:20px;width:100%;background-color:#fff>" \
                  "<div style=margin-left:0;padding-top:50px;padding-bottom:20px>" \
                  "<img src={logo}" \
                  " style=margin-left:-10px;margin-top:20px;height:40px>" \
                  "<p style=font-family:sans-serif;margin-left:0;padding-top:15px;color:#424242>" \
                  "Hallo <span style=font-weight:700>{names},</span>" \
                  "<p style=font-family:sans-serif;margin-left:0;color:#424242>" \
                  "Welcome to Save<p style=font-family:sans-serif;margin-left:0;color:#424242>" \
                  "Reset your password, and we'll get you on your way.<br>" \
                  "To change your Save password, click *" \
                  "<a href={link}>here</a>* or paste the following link into your browser:<br>" \
                  "{link}<p style=font-family:sans-serif;margin-left:0;color:#424242>" \
                  "{footer}</div></div><div style=padding-left:20px;width:100%;padding-top:5px;" \
                  "background-color:#FAFAFA><div style=margin-left:0;margin-top:10px;margin-bottom:10px>" \
                  "<span style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>" \
                  "You\'re receiving this message because you are a save user send us " \
                  "feedback on info@getsave.io or call us +250785489992</span>" \
                  "<p style=font-family:sans-serif;font-size:12px;margin-left:0;" \
                  "color:#424242>Save is a product of " \
                  "<a href=http://www.exuus.com target=_blank>exuus Ltd.</a>" \
                  "<br>Exuus is a limited corporation registered in Republic of Rwanda.</div></div>".format(
            names=self.names, link=self.recover, footer=self.footer, logo=self.logo)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)

        return self.key

    def resetsuccess(self):

        msg = Message('Password reset successful', sender='Save Team', recipients=[self.email])
        content = "<div style=padding-left:20px;width:100%;background-color:#fff>" \
                  "<div style=margin-left:0;padding-top:50px;padding-bottom:20px>" \
                  "<img src={logo} style=margin-left:-10px;margin-top:20px;height:40px><p style=font-family:sans-serif;margin-left:0;padding-top:15px;color:#424242>Hallo <span style=font-weight:700>{names},</span><p style=font-family:sans-serif;margin-left:0;color:#424242>Welcome to Savetix<p style=font-family:sans-serif;margin-left:0;color:#424242>You've successfully changed your Save password.<br>{link}<p style=font-family:sans-serif;margin-left:0;color:#424242>{footer}</div></div><div style=padding-left:20px;width:100%;padding-top:5px;background-color:#FAFAFA><div style=margin-left:0;margin-top:10px;margin-bottom:10px><span style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>You\'re receiving this message because you are a Save user send us feedback on info@getsave.io or call us +250785489992</span><p style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>Save is a product of <a href=http://www.exuus.com target=_blank>exuus Ltd.</a><br>Exuus is a limited corporation registered in Republic of Rwanda.</div></div>".format(
            names=self.names, link=self.login, footer=self.footer, logo=self.logo)
        msg.html = """ {content} """.format(content=content)
        mail.send(msg)
        return True


def help(names, email, title, message):
    logo = "https://getsave.io/img/save_blue.svg"
    footer = "For any inquiry e-mail us on info@getsave.io or call us on +250 785-489-992<p>Thanks for using Save, enjoy.<br>Save Team"
    msg = Message('[Save][Support]', sender='Save Support', recipients=['support@getsave.io'])
    msg.add_recipient(email)
    content = '<div style=padding-left:20px;width:100%;background-color:#fff>' \
              '<div style=margin-left:0;padding-top:50px;padding-bottom:20px>' \
              '<img src={logo} style=margin-left:-10px;margin-top:20px;height:40px>' \
              '<p style=font-family:sans-serif;margin-left:0;padding-top:15px;color:#424242>Hallo <span style=font-weight:700>{names},</span>' \
              '<p style=font-family:sans-serif;margin-left:0;color:#424242>{title}</p>' \
              '<p style=font-family:sans-serif;margin-left:0;color:#424242>"{message}"</p>' \
              '<p style=font-family:sans-serif;margin-left:0;color:#424242>{footer}</div></div>' \
              '<div style=padding-left:20px;width:100%;padding-top:5px;background-color:#FAFAFA>' \
              '<div style=margin-left:0px;margin-top:10px;margin-bottom:10px;>' \
              '<span style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>You\'re receiving this message because you are a Save user send us feedback on info@getsave.io or call us +250785489992</span>' \
              '<p style=font-family:sans-serif;font-size:12px;margin-left:0;color:#424242>Save is a product of <a href=http://www.exuus.com target=_blank>exuus Ltd.</a>' \
              '<br>Exuus is a limited corporation registered in Republic of Rwanda.</p></div></div>'.format(names=names, title=title, message=message, footer=footer, logo=logo)
    msg.html = """ {content} """.format(content=content)
    mail.send(msg)
    return True