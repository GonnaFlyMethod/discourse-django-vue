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
			add_view_to_topic_api = reverse('discourse:add-view-to-topic',
				                   kwargs={'topicID': topic.id});

			context = {
				'topic': topic,
				'info':info,
				'comments': comments,
			    'send_comment_link': send_comment_link,
			    'add_view_to_topic_api': add_view_to_topic_api,
			}
			return render(request, 'discourse/detail.html', context)
		elif type_ == 'topic_info':
			return Response(topic_info.data)
		else:
			comments = topic_info.get_comments(topic)
			comments_clean = comments
			for dict_ in comments_clean: 
				dict_['send_like_api'] = reverse('discourse:like-comment',
				                   kwargs={'commentID': dict_['id']})
				url_unlike_comment = reverse('discourse:unlike-comment',
				                   kwargs={'commentID': dict_['id']})
				dict_['unlike_comment_api'] = url_unlike_comment

				time_edge = re.search(r'T', dict_['timestamp'])
				dict_['timestamp'] = dict_['timestamp'][:time_edge.start()]


				comment = Comment.objects.get(id=dict_['id'])
				if request.user in comment.who_liked.all():
					dict_['who_liked'] = str(request.user)
				else:
					dict_['who_liked'] = ''

			lambda_func = lambda x: x['id']
			comments_clean = sorted(comments_clean, key=lambda_func)
			return Response(comments_clean)


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


class LikeCommentAPI(APIView):

	def patch(self, request, commentID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			comment = Comment.objects.get(id=commentID)

			if usr not in comment.who_liked.all():
				comment.who_liked.add(usr)
				comment.likes += 1
				comment.save()
				data['status'] = 'OK'
				return Response(data)
			else:
				HttpResponseBadRequest()
		else:
			return HttpResponseBadRequest()

class UnlikeCommentAPI(APIView):

	def patch(self, request, commentID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			comment = Comment.objects.get(id=commentID) 
			if usr in comment.who_liked.all():

				comment.who_liked.remove(usr)
				comment = Comment.objects.get(id=commentID)
				comment.likes -= 1
				comment.save()
				data['status'] = 'OK'
				return Response(data)
			else:
				return HttpResponseBadRequest()
		else:
			return HttpResponseBadRequest()


class AddViewToTopicAPI(APIView):

	def patch(self, request, topicID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			topic = Topic.objects.get(id=topicID)

			if usr not in topic.who_viewed.all():
				topic.who_viewed.add(usr)
				topic.views += 1
				topic.save()
				data['status'] = 'OK'
			else:
				data['status'] = 'VIEWED'
		else:
			data['status'] = 'NOT AUTHENICATED'
		return Response(data)


class CreateTopicAPI(APIView):

	template = 'discourse/create_topic.html'

	def get(self, request):
		return render(request, self.template)

	def post(self, request):
		usr = request.user

		if usr.is_authenticated:
			topic_data = {'topic': request.data['topic']}
			comment_from_req = request.data['text']
			comment_data = {
				'text': comment_from_req
			}
			create_topic = TopicsSerializer(data=topic_data)

			comment = PostCommentSerializer(data=comment_data)
			data = {}
			id_of_topic = None
			if create_topic.is_valid():
				create_topic.validated_data['author'] = usr
				if comment.is_valid():
					create_topic.save()
					id_of_topic = create_topic.data['id']
					data['url_redirect'] = reverse('discourse:topic-detail',
					                            kwargs={'topicID': id_of_topic,
					                                    'type_': 'get'})

					comment.validated_data['author'] = usr

					topic = Topic.objects.get(id=create_topic.data['id'])
					comment.validated_data['to_topic'] = topic
					comment.save()
					data['status'] = 'OK'
					return Response(data)
				else:
					return Response(comment.errors)
			else:
				return Response(create_topic.errors)
		else:
			return HttpResponseBadRequest()
