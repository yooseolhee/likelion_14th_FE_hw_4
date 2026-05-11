from django.urls import path

from . import views

urlpatterns = [
    # 페이지
    path('', views.home, name='home'),
    path('tech/', views.tech_list, name='tech_list'),
    path('tech/<slug:slug>/', views.tech_detail, name='tech_detail'),
    path('projects/', views.projects_list, name='projects_list'),
    path('about/', views.profile, name='profile'),
    path('daily/', views.daily_list, name='daily_list'),

    # 인증
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # JSON API (2주차 — fetch로 호출)
    # GET  /api/posts/<slug>/comments/  → 댓글 목록
    # POST /api/posts/<slug>/comments/  → 댓글 추가 (로그인 필요)
    path('api/posts/<slug:slug>/comments/', views.comments_api, name='comments_api'),
]
