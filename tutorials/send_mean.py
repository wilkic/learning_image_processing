
import smtplib
import getpass

from email.mime.text import MIMEText

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
    #server.login("info@goodspeedparking.com", "Pass1word")
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


def send_msg( message ):

    srvDict = setup_server()

    msg = MIMEText(message)
    msg['Subject'] = "test message from viper"
    msg['From'] = srvDict['sender']
    msg['To'] = ', '.join(srvDict['recipients'])


    srvDict['server'].sendmail( srvDict['sender'], 
                                srvDict['recipients'],
                                msg.as_string() )

    return
