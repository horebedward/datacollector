import yagmail


def send_email(email, height, avg_height, count):

    subject = 'Height data'
    message = 'Hey there, your height is <strong>%s</strong>.And Average height of all is %s. Out of %s people' % (height, avg_height, count)

    yag = yagmail.SMTP(#Email, #Password)
    yag.send(email, subject, message)

