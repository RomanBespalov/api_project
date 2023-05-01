from django.core.mail import send_mail


def send_confirm_code_to_email(user, email):
    send_mail(
        'Confirmation code for registration on Yamdb',
        user.confirmation_code,
        'from@example.com',
        [email],
        fail_silently=False
    )
