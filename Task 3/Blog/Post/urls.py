from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import HomeView, PostView, CreatePost, LoginView, RegistrationView, DeletePost, UpdatePost

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', PostView.as_view(), name='post_details'),
    path('post/create/', CreatePost.as_view(), name='create_post'),
    path('delete-post/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('update-post/<int:pk>/', UpdatePost.as_view(), name='update_post'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
