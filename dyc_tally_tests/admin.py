from django.contrib import admin
from .models import TestType, TestQuestion, TestOption, TestResponse, TestAttempt

# Register your models here.

admin.site.register(TestType)
admin.site.register(TestQuestion)
admin.site.register(TestOption)
admin.site.register(TestAttempt)
admin.site.register(TestResponse)
