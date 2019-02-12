from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit/<int:instagram_account_id>', views.edit_instagram_account, name='edit_instagram_account'),
    path('accounts/profile/delete/<int:instagram_account_id>', views.delete_instagram_account, name='delete_instagram_account'),
    path('accounts/profile/edit/<int:instagram_account_id>/tag', views.add_tag, name='add_tag')
]

