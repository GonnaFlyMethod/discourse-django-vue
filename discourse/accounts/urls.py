from django.urls import path, re_path

from . import views


app_name = 'accounts'

urlpatterns = [
   path('sign-up/', views.SignUpFormView.as_view(), name='sign-up')

]

rest_api_urls = [
    re_path(r'api/get-countries/?',
            views.GetCountriesAPI.as_view(), name='get-countries'),
    # re_path(r'api/sign-up/?', views.SignUpApiView.as_view(),
    #         name='sign-up-api')
]

urlpatterns += rest_api_urls
