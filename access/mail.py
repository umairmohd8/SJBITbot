import smtplib
import time
from private import keys


def sendMail(usr_mail, usr_code):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(keys.EMAIL_ADDRESS, keys.EMAIL_PASSWORD)

            subject = 'SJBIT Discord passcode.'
            body = f'Your passcode is: {usr_code}\nTo verify yourself use: "+code:{usr_code}"' \
                   f' in #verify-yourself channel'

            msg = f'Subject: {subject}\n\n{body}'

            smtp.sendmail(keys.EMAIL_ADDRESS, usr_mail, msg)
            # time.sleep(140)
        return 'Code sent', 0
    except Exception as e:
        return e, -1
