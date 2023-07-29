from django.core.mail import send_mail
from django.conf import settings






def send_email_verify(email, token):
    subject = 'Get-Hired Verify your email'
    message = f'Click to verify your email: http://localhost:5173/verify-email/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



def send_resume_downloaded(email,company,application_designation):
    subject = 'Get-Hired resume downloaded'
    message = f'Congratulations! We are thrilled to inform you that your resume has been downloaded by {company} for the application to the position of {application_designation}. This is an exciting opportunity, and we wish you the best of luck in the selection process. We believe your skills and experience make you a strong candidate, and we look forward to seeing your continued success. Should you have any questions or require further information, please dont hesitate to reach out. Thank you for choosing our platform, and we hope this leads you to your dream job!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True