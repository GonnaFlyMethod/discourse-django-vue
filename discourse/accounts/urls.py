from django.urls import path, re_path

from . import views


app_name = 'accounts'

urlpatterns = [
   path('sign-up/', views.SignUpFormView.as_view(), name='sign-up'),
   path('sign-in/', views.SignInView.as_view(), name='sign-in'),
   path('logout/', views.LogoutView.as_view(), name='logout'),
   path('<int:user_id>/', views.UserProfileView.as_view(),
        name='user-profile'),

]

rest_api_urls = [
    re_path(r'api/get-countries/?',
            views.GetCountriesAPI.as_view(), name='get-countries'),
    re_path(r'api/get-user-details/(?P<user_id>\d+)/?',
            views.UserProfileAPI.as_view(), name='user-profile-api'),
]

urlpatterns += rest_api_urls
