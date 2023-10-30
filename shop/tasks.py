from django.core.mail import send_mail

def send_email_task(email, subject, message):
    send_mail(subject, message, 'sender@example.com', [email])
