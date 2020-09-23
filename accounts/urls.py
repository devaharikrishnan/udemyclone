from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('ratings/<str:title>', views.review, name='rattings'),
    path('feedback/<str:title>', views.feedback, name='feedback'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('videos', TemplateView.as_view(template_name="lessons/video.html"), name='videos'),
    path('users/', include([
        path('my-courses', views.EnrolledCoursesListView.as_view(), name='enrolled-courses'),
        path('my-courses/<slug:slug>/view', views.StartLessonView.as_view(), name='course-lessons'),
        path('my-courses/<slug:slug>/lessons/<int:id>', views.LessonView.as_view(), name='course-lessons-single'),
        path('profile', views.ProfileUpdateView.as_view(), name='my-profile'),
        path('viewmycourses', views.viewmycourses, name='viewmycourses'),
        path('createcourse', views.Createcourse, name='createcourse'),
        path('editcourse/<str:title>', views.Editcourse, name='editcourse'),
        path('createlesson/<str:title>', views.Createlesson, name='createlesson'),
        path('viewmylesson/', views.viewmylessons, name='viewmylessons'),
        path('editlesson/<str:title>/<int:pk>', views.Editlesson, name='editlesson'),
    ])),
]
