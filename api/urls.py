from django.urls import path
from . import views

urlpatterns = [
    path("getSlang/", views.getSlang, name="getSlang"),
    path("sendSMS/", views.sendSMS, name="sendSMS"),
    path("getUrl/", views.getUrl, name="getUrl"),
    path("addResponse/", views.addResponse, name="addResponse"),
    path("validateRecords/", views.validateRecords, name="validateRecords"),
    path("responseForm/", views.responseForm, name="responseForm"),
    path("slangForm/", views.slangForm, name="slangForm"),
    path("smsForm/", views.smsForm, name="smsForm"),
    path("googleSheetUrl/", views.googleSheetUrl, name="sheetUrl"),
    path("", views.home),
]
