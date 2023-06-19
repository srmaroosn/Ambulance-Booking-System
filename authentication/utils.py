from django.core.mail import EmailMessage

class Util:
    #defining method to send mail
    #defining static method so we dont need to call the class
    @staticmethod
    def send_email(data):
        email= EmailMessage(subject=data['email_subject'], body= data['email_body'], to=[data['to_email']])
        email.send()