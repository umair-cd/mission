from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^questions/$", views.QuestionList.as_view(), name="questions-list"),
]
