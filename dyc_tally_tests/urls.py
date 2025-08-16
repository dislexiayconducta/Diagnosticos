from django.urls import path
from .views import dyc_test_tally_view

urlpatterns = [
    path("test/dyc/", dyc_test_tally_view, name="webhook_test"),
]
