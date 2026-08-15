from django.urls import path
from . import views
urlpatterns=[
 path('',views.home,name='home'),path('about/',views.about,name='about'),path('course/',views.about,name='course_legacy'),path('program/',views.program,name='program'),path('teachers/',views.teachers,name='teachers'),path('teachers/<slug:slug>/',views.teacher_detail,name='teacher_detail'),path('faq/',views.faq,name='faq'),
 path('news/',views.news_list,name='news'),path('news/<slug:slug>/',views.news_detail,name='news_detail'),path('register/',views.register,name='register'),path('register/success/',views.registration_success,name='registration_success'),path('contact/',views.contact,name='contact'),path('robots.txt',views.robots,name='robots'),path('sitemap.xml',views.sitemap,name='sitemap'),]
