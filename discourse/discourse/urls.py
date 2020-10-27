from django.urls import path, re_path

from . import views


app_name = 'discourse'

urlpatterns = [
	path('main/', views.MainPageView.as_view(), name='main')
]

rest_api_urls = [
	re_path(r'api/get-topics/?', views.GetTopicsApi.as_view(),
		    name='get-topics-api')
]

urlpatterns += rest_api_urls
