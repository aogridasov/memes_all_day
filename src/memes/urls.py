from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'memes'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('liked/', views.FavoritesView.as_view(), name='favorites'),
    path('uploaded/', views.MyUploadsView.as_view(), name='my_memes'),
    path('upload/', views.MemeUploadView.as_view(), name='upload_meme'),
    path('search/', views.SearchView.as_view(), name='search'),
    path(
        'signup/', views.SignUp.as_view(template_name='auth/signup.html'), name='signup'
    ),
    path('logout/', LogoutView.as_view(next_page='memes:index'), name='logout'),
    path(
        'login/',
        LoginView.as_view(template_name='auth/login.html', next_page='memes:index'),
        name='login',
    ),
    path('create/', views.meme_create, name='meme_create'),
    path('meme/<int:id>/delete/', views.meme_delete, name='meme_delete'),
    path('meme/<int:id>/like/', views.like_meme, name='like_meme'),
    path('meme/<int:id>/unlike/', views.unlike_meme, name='unlike_meme'),
]
