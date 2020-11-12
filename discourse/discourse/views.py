import re

from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from accounts.models import Account

from .serializers import (TopicsSerializer, CommentToTopicSerializer,
	                      PostCommentSerializer, AttachTagsToTopicSerializer)

from .models import Topic, Comment, TagOfTopic


class MainPageView(View):
	def get(self, request):
		return render(request, 'discourse/main.html')


class GetTopicsApi(ListAPIView):
	queryset = Topic.objects.all()
	pagination_class = PageNumberPagination
	serializer_class = TopicsSerializer


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
				e = dict_['author']   # e-mail
				author_of_comment = Account.objects.get(email=e)
				author_id = author_of_comment.id
				dict_['author_prof_url'] = reverse('accounts:user-profile',
				                   kwargs={'user_id': author_id})

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
			sphere_data = request.data['main_sphere_of_topic']
			tags_of_topic = request.data['tags']
			topic_data = {'topic': request.data['topic'],
			              'main_sphere_of_topic': sphere_data,
			              'tags': tags_of_topic}
			comment_from_req = request.data['text']
			comment_data = {
				'text': comment_from_req
			}

			create_topic = TopicsSerializer(data=topic_data)

			comment = PostCommentSerializer(data=comment_data)
			data = {}
			id_of_topic = None
			if create_topic.is_valid():
				if not tags_of_topic:
					data['status'] = 'tags_error'
					data['tags_error'] = ['This field may not be blank.']
					return Response(data)

				create_topic.validated_data['author'] = usr
				if comment.is_valid():
					create_topic.save()
					id_of_topic = create_topic.data['id']
					data['url_redirect'] = reverse('discourse:topic-detail',
					                            kwargs={'topicID': id_of_topic,
					                                    'type_': 'get'})

					topic = Topic.objects.get(id=create_topic.data['id'])
					topic.self_url = reverse('discourse:topic-detail',
	 			                   kwargs={'topicID':topic.id,'type_': 'get'})
					
					date = self.get_clean_day_and_month(topic)
					topic.day_of_publication = date['day']
					topic.month_of_publication = date['month']
	
					topic.save()

					comment.validated_data['author'] = usr
					comment.validated_data['to_topic'] = topic
					comment.save()
					usr.topics_created.add(topic)
					tags_are_valid: dict = self.tags_are_valid(tags_of_topic,
						                                       topic)

					if tags_are_valid['status']:
						data['status'] = 'OK'
					else:
						data['status'] = 'tags_error'
						data['tags_error'] = tags_are_valid['errors']
					return Response(data)
				else:
					return Response(comment.errors)
			else:
				return Response(create_topic.errors)
		else:
			return HttpResponseBadRequest()

	def get_clean_day_and_month(self, topic_obj) -> dict:

		# Date & time of publication of topic
		time_stamp = topic_obj.timestamp
		day = time_stamp.strftime("%d")
		month = time_stamp.strftime("%b")
		if day.startswith('0'):
			day = day[1:]

		res = {'day': day, 'month': month}
		return res

	def tags_are_valid(self, tags_raw: str, topic) -> dict:
		tags_clean:list = tags_raw.split(',')
		initial_check_of_tags = {}
		for i in tags_clean:
			if isinstance(i, str):
				initial_check_of_tags.setdefault(i, 'OK')

		if len(tags_clean) == len(initial_check_of_tags):
			existing_tags = TagOfTopic.objects.all()
			for tag in tags_clean:
				if tag not in existing_tags:
					data = {'name_of_tag': tag}
					serializer = AttachTagsToTopicSerializer(data=data)

					if serializer.is_valid():
						serializer.save()
						tag = TagOfTopic.objects.get(id=serializer.data['id'])
						topic.tags.add(tag)
					else:
						return {'status': False,
						'errors': serializer.errors['name_of_tag']}
				else:
					tag = TagOfTopic.objects.get(name_of_tag=tag)
					topic.tags.add(tag)
			return {'status': True}

		else:
			return {'status': False, 'errors': 'Wrong input of tags'}