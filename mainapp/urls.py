from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig


app_name = MainappConfig.name

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('contacts/', views.ContactsPageView.as_view(), name="contacts"),
    path('courses/', views.CoursesListPageView.as_view(), name="courses"),
    path('doc_site/', views.DocSitePageView.as_view(), name="doc_site"),
    path('news/', views.NewsPageView.as_view(), name="news"),
    path("news/<int:page>/", views.NewsWithPaginatorView.as_view(), name="news_paginator"),
    path('login/', views.LoginPageView.as_view(), name="login"),
    path('search/', views.search, name="search")
]
