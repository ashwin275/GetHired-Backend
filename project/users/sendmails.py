from django.core.mail import send_mail
from django.conf import settings






def send_email_verify(email, token):
    subject = 'Get-Hired Verify your email'
    message = f'Click to verify your email: https://gethiredin.netlify.app/verify-email/{token}/'
    # message = f'Click to verify your email: http://localhost:5173/verify-email/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



def send_employer_action_mail(email,message,subject):
    print(email,subject,message)
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    print('true inside function')
    return True