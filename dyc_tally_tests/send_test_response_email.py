from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from decouple import config


class EmailTestResponse:
    @staticmethod
    def send_test_response_email(selected_template, email, score):
        subject = "Respuesta de test "
        context = {
            "email": email,
            "score": score,
            "pagent": "Dislexia y Conducta",
        }

        html_message = render_to_string(
            f"diagnostics_email_responses/plantilla_{selected_template}.html", context
        )

        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=config("EMAIL_USER"),
            to=[email],
        )
        email.content_subtype = "html"
        email.send()
