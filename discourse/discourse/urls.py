from django.urls import path, re_path

from . import views


app_name = 'discourse'

urlpatterns = [
	path('main/', views.MainView.as_view(), 
		 name='main'),
	# Sections
	path('<str:section>/', views.ParticularSphereView.as_view(), 
		 name='particular-section'),
	path('topics/not-approved', views.NotApprovedTopicsApi.as_view(),
		 name='not-approved-page'),
	path('', views.TopicDetail.as_view(), name='topic-detail'),
	path('topics/<int:topicID>/<str:type_>/',
	        views.TopicDetail.as_view(), name='topic-detail'),
]


rest_api_urls = [
	re_path(r'api/get-sections/?', views.GetSectionsAPI.as_view(),
		     name='get-sections'),

	re_path(r'api/get-topics/(?P<name_of_section>\w+)/?',
		    views.GetTopicsApi.as_view(), name='get-topics-api'),
	re_path(r'create-topic/?', views.CreateTopicAPI.as_view(),
			name='create-topic'),
	re_path(r'api/get-not-approved-topics/?', 
		    views.GetNotApprovedTopicsApi.as_view(),
		    name='get-not-approved-topics-api'),

	# Topic approvement / disapprovement
	re_path(r'api/approve-topic/?',
		    views.ApproveTopicAPI.as_view(),
		    name='approve-topic-api'),
	re_path(r'api/dispprove-topic/',
		    views.DisApproveTopicAPI.as_view(), name='dispprove-topic-api'),

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
