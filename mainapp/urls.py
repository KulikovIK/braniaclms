from mainapp import views
from django.urls import path
from mainapp.apps import MainappConfig


app_name = MainappConfig.name

urlpatterns = [
    path('', views.MainPageView.as_view(), name="main_page"),
    path('contacts/', views.ContactsPageView.as_view(), name="contacts"),

    # Courses
    path('courses/', views.CoursesListPageView.as_view(), name="courses"),
    path('courses/<int:pk>/detail/', views.CourseDetailView.as_view(), name="courses_detail"),
    path('courses/feedback/', views.CourseFeedbackCreateView.as_view(), name="course_feedback"),

    path('doc_site/', views.DocSitePageView.as_view(), name="doc_site"),
    path('login/', views.LoginPageView.as_view(), name="login"),
    path('search/', views.search, name="search"),

    # News
    path('news/', views.NewsListView.as_view(), name="news"),
    path('news/add/', views.NewsCreateView.as_view(), name="news_create"),
    path('news/<int:pk>/update/', views.NewsUpdateView.as_view(), name="news_update"),
    path('news/<int:pk>/detail/', views.NewsDetailView.as_view(), name="news_detail"),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name="news_delete"),
]
