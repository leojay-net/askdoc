from django.urls import path
from .views import (AddAdminUser, User_Update, User_Retrieve, Login, Logout, CreateUser, AdminUsers, RemoveAdminUser, FetchUsers, UserProfileUpdate, FetchUserProfile, CreateUserProfile, CreateToken, resetpassword)

urlpatterns = [
    path('register_user/', CreateUser.as_view(), name="add-user"),
    path('authenticate/user/login', Login.as_view(), name="auth-user"),
    path('authenticate/user/logout', Logout.as_view(), name="logout-user"),
    path('user/update/<str:id>', User_Update.as_view(), name='update_user'),
    path('user/get/<str:id>', User_Retrieve.as_view(), name='retrieve_user'),
    path('add_admin/<str:pk>', AddAdminUser.as_view(), name="add-admin"),
    path('remove_admin/<str:pk>', RemoveAdminUser.as_view(), name="add-admin"),
    path('all_users/', FetchUsers.as_view(), name="all-users"),
    path('profile/update/<str:id>', UserProfileUpdate.as_view(), name='update_profile'),
    path('profile/get/<str:id>', FetchUserProfile.as_view(), name='retrieve_profile'),
    path('create/user/profile', CreateUserProfile.as_view(), name="add-profile"),
    path('create/token', CreateToken.as_view(), name="add-token"),
    path('reset/password', resetpassword.as_view(), name="reset-password"),
    # path('Verify_token/<int:token>', VerifyToken.as_view(), name="verufy_token")
]