import re
import calendar

from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import Account

from .serializers import (TopicsSerializer, CommentToTopicSerializer,
	                      PostCommentSerializer)

from .models import Topic, Comment


class MainPageView(View):
	def get(self, request):
		return render(request, 'discourse/main.html')


class GetTopicsApi(APIView):

	def get(self, request):
		get_all_topics = Topic.objects.all()
		serializer = TopicsSerializer(get_all_topics, many=True)

		data_to_display = serializer.data
		for num_of_iter, dict_ in enumerate(data_to_display):
			find_day = re.search(r'-\d{1,2}T', dict_['timestamp'])
			day_start = find_day.start() + 1
			day_end = find_day.end() - 1

			find_month = re.search(r'-\d{1,2}-', dict_['timestamp'])
			month_start = find_month.start() + 1
			month_end = find_month.end() - 1
			new_timestamp:str = dict_['timestamp'][day_start:day_end]
			month = dict_['timestamp'][month_start:month_end]
			dict_['timestamp'] = new_timestamp
			dict_['month'] = calendar.month_abbr[int(month)]
			topic_id = int(dict_['id'])
			dict_['url'] = reverse('discourse:topic-detail',
				                   kwargs={'topicID':topic_id,'type_': 'get'})
		return Response(data_to_display)


class TopicDetail(APIView):

	def get(self, request, topicID, type_):
		topic = Topic.objects.get(id=topicID)
		topic_info = TopicsSerializer(topic)
		if type_ == 'get':
			info = reverse('discourse:topic-detail',
				           kwargs={'topicID': topic.id, 'type_':'topic_info'})
			comments = reverse('discourse:topic-detail',
				           kwargs={'topicID': topic.id, 'type_':'comments'})
			send_comment_link = reverse('discourse:post-comment',
				                   kwargs={'topicID': topic.id}) 
			context = {'topic': topic, 'info':info,'comments': comments,
			           'send_comment_link': send_comment_link}
			return render(request, 'discourse/detail.html', context)
		elif type_ == 'topic_info':
			return Response(topic_info.data)
		else:
			comments = topic_info.get_comments(topic)
			return Response(comments)



class PostCommentAPI(APIView):

	def post(self, request, topicID):
		if request.user.is_authenticated:
			account = Account.objects.get(id=request.user.id)
			topic = Topic.objects.get(id=topicID)
			serializer = PostCommentSerializer(data=request.data)

			if serializer.is_valid():
				serializer.validated_data['author'] = account
				serializer.validated_data['to_topic'] = topic
				serializer.save()
				return Response({'status':'OK'})
			else:
				return Response(serializer.errors)
		else:
			return HttpResponseBadRequest()
