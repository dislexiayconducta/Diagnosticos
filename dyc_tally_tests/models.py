from django.db import models


# Create your models here.
class TestType(models.Model):
    form_name = models.CharField(max_length=100)
    form_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.form_name}"


class TestQuestion(models.Model):
    question = models.CharField(max_length=250)
    test_type = models.ForeignKey(
        TestType, on_delete=models.CASCADE, related_name="questions"
    )
    question_key = models.CharField(max_length=100, unique=True)
    test_answer_value = models.CharField(
        max_length=250, unique=True, null=True, blank=True
    )  # respuesta hecha por el cliente

    def __str__(self) -> str:
        return f"{ self.question } - {self.question_key}"


class TestOption(models.Model):
    weighing = models.PositiveBigIntegerField(default=0)
    name_text = models.CharField(max_length=100)
    test_question = models.ForeignKey(
        TestQuestion, on_delete=models.CASCADE, related_name="options"
    )
    option_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name_text} con una ponderación de {self.weighing}"


class TestAttempt(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    education = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"


class TestResponse(models.Model):
    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    option = models.ForeignKey(
        TestOption, on_delete=models.CASCADE, null=True, blank=True
    )
    answer_text = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.question.question} - {self.answer_text}"
