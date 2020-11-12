from django.urls import path, re_path

from . import views


app_name = 'discourse'

urlpatterns = [
	path('main/', views.MainView.as_view(), 
		 name='particular-section'),
	# Sections
	path('<str:section>/', views.ParticularSphereView.as_view(), 
		 name='particular-section'),

	path('',
	        views.TopicDetail.as_view(), name='topic-detail'),
	path('topics/<int:topicID>/<str:type_>/',
	        views.TopicDetail.as_view(), name='topic-detail'),
]

rest_api_urls = [
	re_path(r'api/get-topics/?', views.GetTopicsApi.as_view(),
			name='get-topics-api'),
	re_path(r'create-topic/?', views.CreateTopicAPI.as_view(),
			name='create-topic'),
	re_path(r'add-view-to-topic/(?P<topicID>\d+)/?',
			views.AddViewToTopicAPI.as_view(), name='add-view-to-topic'),
	re_path(r'topics/post-comment/(?P<topicID>\d+)/?',
			views.PostCommentAPI.as_view(), name='post-comment'),
	re_path(r'topics/like-comment/(?P<commentID>\d+)/?',
			views.LikeCommentAPI.as_view(), name='like-comment'),
	re_path(r'topics/unlike-comment/(?P<commentID>\d+)/?',
			views.UnlikeCommentAPI.as_view(), name='unlike-comment'),
]

urlpatterns += rest_api_urls
