
import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def print_mean( mean ):
    
    body = \
    """
    The mean value is currently equal to %f.\n
    """ % mean

    print '%s' % body

    return

def setup_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    sender = "goodspeedviper@gmail.com"
    pwd = getpass.getpass()

    #Next, log in to the server
    server.login( sender, pwd )
    
    srvDict = {'server':server,
               'sender':sender}

    return srvDict



def send_mean( mean, recipients ):

    srvDict = setup_server()

    body = \
    """
    Viper system test:
    The mean value is currently equal to %f.\n
    """ % mean

    msg = MIMEText(body)
    msg['Subject'] = "test message from viper"
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)


    srvDict['server'].sendmail( srvDict['sender'], 
                                recipients,
                                msg.as_string() )

    return


def send_msg( message, recipients ):

    srvDict = setup_server()

    msg = MIMEText(message)
    msg['Subject'] = "test message from viper"
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)


    srvDict['server'].sendmail( srvDict['sender'], 
                                recipients,
                                msg.as_string() )

    return

def send_msg_with_jpg( message, fname, recipients  ):

    srvDict = setup_server()

    msg = MIMEMultipart()
    body = MIMEText(message,'plain')
    msg['Subject'] = "test message from viper"
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(recipients)
    msg.attach(body)
    msg.attach(MIMEImage(file(fname).read(), _subtype="jpeg"))

    srvDict['server'].sendmail( srvDict['sender'], 
                                recipients,
                                msg.as_string() )
    srvDict['server'].close()

    return

