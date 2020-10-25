from django.urls import path, re_path

from . import views


app_name = 'accounts'

urlpatterns = [
   path('sign-up/', views.SignUpFormView.as_view(), name='sign-up-form')

]

rest_api_urls = [
    re_path(r'api/get-countries/(?P<operation>)(sign-up)/?',
            views.GetCountriesAPI.as_view(), name='get-countries')
]

urlpatterns += rest_api_urls
