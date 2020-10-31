from django.urls import path, re_path

from . import views


app_name = 'discourse'

urlpatterns = [
	path('main/', views.MainPageView.as_view(), name='main'),
	path('topics/<int:topicID>/<str:type_>/',
	        views.TopicDetail.as_view(), name='topic-detail')
]

rest_api_urls = [
	re_path(r'api/get-topics/?', views.GetTopicsApi.as_view(),
		    name='get-topics-api'),
	re_path(r'topics/post-comment/(?P<topicID>\d+)/?',
		    views.PostCommentAPI.as_view(), name='post-comment')
]

urlpatterns += rest_api_urls
