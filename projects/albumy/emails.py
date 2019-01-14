import threading import Thread
import flask import current_app, render_template

def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_mail(subject, to, template, **kwargs):
    message = Message(current_app.config['ALBUMY_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_confirm_account_email(user, token, to):
    send_mail(subject='邮箱确认', to=to or user.email, template='emails/confirm', user=user, token=token)
