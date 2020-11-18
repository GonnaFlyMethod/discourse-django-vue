import re

from django.views import View
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from accounts.models import Account

from .serializers import (TopicsSerializer, CommentToTopicSerializer,
	                      PostCommentSerializer, AttachTagsToTopicSerializer,
	                      SectionsSerializer)

from .models import Topic, Comment, TagOfTopic, TopicSection


class MainView(View):
	
	template = 'discourse/main.html'
	def get(self, request):

		return render(request, self.template)


class GetSectionsAPI(APIView):
	permission_classes = [AllowAny]

	def get(self, request):
		default_sections = ['Travel', 'People', 'Education', 'Video games']
		sections = TopicSection.objects.all()
		serializer = SectionsSerializer(sections, many=True)

		serializer_data = serializer.data
		for section in serializer_data:
			s_name = section['name_of_section']
			if s_name not in default_sections:
				img_url = section['image_of_section'].url
				section['image_of_section_url'] = img_url
			else:
				section['image_of_section_url'] = section['image_of_section']

			section['url'] = reverse('discourse:particular-section',
				                     kwargs={'section': s_name})

			sections_obj = get_object_or_404(TopicSection, 
				                             name_of_section=s_name)
			section['total_topics'] = sections_obj.get_total_num_of_topics()

		return Response(serializer_data)


class ParticularSphereView(View):
	def get(self, request, section):
		context = {'section': section,
				   'get_topics_api': reverse('discourse:get-topics-api',
				   	                       args=(section,))}
		return render(request, 'discourse/particular_sphere.html', context)


class GetTopicsApi(ListAPIView):
	permission_classes = [AllowAny]
	pagination_class = PageNumberPagination
	serializer_class = TopicsSerializer

	def get_queryset(self):
		section_name = self.kwargs['name_of_section']
		
		section = get_object_or_404(TopicSection, name_of_section=section_name)
		topics = section.topics_included.all().filter(approved=True)
		return topics


class TopicDetail(APIView):
	permission_classes = [AllowAny]

	def get(self, request, topicID, type_):

		currents_user = request.user
		topic = Topic.objects.get(id=topicID)

		if not topic.approved and not topic.author == request.user:
			return HttpResponseBadRequest()

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


				comment = get_object_or_404(Comment, id=dict_['id'])
				if request.user in comment.who_liked.all():
					dict_['who_liked'] = str(request.user)
				else:
					dict_['who_liked'] = ''

			lambda_func = lambda x: x['id']
			comments_clean = sorted(comments_clean, key=lambda_func)
			return Response(comments_clean)


class PostCommentAPI(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request, topicID):
		if request.user.is_authenticated:
			account = get_object_or_404(Account, id=request.user.id)
			topic = get_object_or_404(Topic, id=topicID)

			if not topic.approved:
				return response({'status': 'NOT PUBLISHED'})

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
	permission_classes = [IsAuthenticated]

	def patch(self, request, commentID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			comment = get_object_or_404(Comment, id=commentID)

			if comment.to_topic.approved:
				if usr not in comment.who_liked.all():
					comment.who_liked.add(usr)
					comment.likes += 1
					comment.save()
					data['status'] = 'OK'
					return Response(data)
				else:
					return HttpResponseBadRequest()
			else:
				return HttpResponseBadRequest()
		else:
			return HttpResponseBadRequest()

class UnlikeCommentAPI(APIView):
	permission_classes = [IsAuthenticated]

	def patch(self, request, commentID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			comment = get_object_or_404(Comment, id=commentID)
			if comment.to_topic.approved:
				if usr in comment.who_liked.all():

					comment.who_liked.remove(usr)
					comment.likes -= 1
					comment.save()
					data['status'] = 'OK'
					return Response(data)
				else:
					return HttpResponseBadRequest()
			else:
				return HttpResponseBadRequest()
		else:
			return HttpResponseBadRequest()


class AddViewToTopicAPI(APIView):
	permission_classes = [IsAuthenticated]

	def patch(self, request, topicID):
		usr = request.user
		data = {}
		if usr.is_authenticated:
			topic = get_object_or_404(Topic, id=topicID)

			if topic.approved:
				if usr not in topic.who_viewed.all():
					topic.who_viewed.add(usr)
					topic.views += 1
					topic.save()
					data['status'] = 'OK'
				else:
					data['status'] = 'VIEWED'
			else:
				data['status'] = 'NOT PUBLISHED'
				return Response(data)
		else:
			data['status'] = 'NOT AUTHENICATED'
		return Response(data)


class CreateTopicAPI(APIView):
	permission_classes = [IsAuthenticated]

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

					# Defining the section of topic
					self.define_section(sphere_data, topic)

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

	def define_section(self, sphere_of_topic, topic_obj):
		sections = ['Travel', 'People', 'Education', 'Video games']
		sections_default_pics: dict = {
			'Travel': 'https://static.vecteezy.com/system/resources/previews/' \
			          '000/224/397/original/compass-travel-vector-illustratio' \
			          'n.jpg',
			'People': 'https://img.freepik.com/free-vector/people-waving-hand-' \
			          'illustration-concept_52683-29825.jpg?size=626&ext=jpg',
			'Education': 'https://i.pinimg.com/originals/4b/4b/c8/4b4bc8f0e26' \
			             'e86fcbdfb5b7a898ee910.jpg',
			'Vid-games': 'https://image.freepik.com/free-vector/colorful-ba' \
			               'ckground-videogame-flat-design_23-2147567954.jpg?1'

		}
		all_sections = TopicSection.objects.all()
		all_sections = [s.name_of_section for s in all_sections]
		for s in sections:
			if s not in all_sections:
				new_section = TopicSection(name_of_section=s)
				new_section.save()

		if sphere_of_topic == 'Travel':
			travel_section = TopicSection.objects.get(name_of_section='Travel')
			travel_section.topics_included.add(topic_obj)
		elif sphere_of_topic == 'People':
			people_section = TopicSection.objects.get(name_of_section='People')
			people_section.topics_included.add(topic_obj)

		elif sphere_of_topic == 'Education':
			edu_section = TopicSection.objects.get(name_of_section='Education')
			edu_section.topics_included.add(topic_obj)
		else:
			# Video games section
			v_games = 'Video games'
			vgames_section = TopicSection.objects.get(name_of_section=v_games)
			vgames_section.topics_included.add(topic_obj)


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


class NotApprovedTopicsApi(View):

	template = 'discourse/not_approved.html'
	def get(self, request):
		get_not_approved_url = reverse('discourse:get-not-approved-topics-api')
		context = {
			'not_approved_topics_api': get_not_approved_url,
		}
		return render(request, self.template, context)


class GetNotApprovedTopicsApi(ListAPIView):
	permission_classes = [IsAdminUser]
	pagination_class = PageNumberPagination
	serializer_class = TopicsSerializer

	def get_queryset(self):
		not_approved_topics = get_list_or_404(Topic, approved=False)
		return not_approved_topics


class ApproveTopicAPI(APIView):

	permission_classes = [IsAdminUser]

	def patch(self, request):

		# Getting data from the dict
		topic_id: int = request.POST.get('id_of_topic', None)
		data: dict = {}
		topic = get_object_or_404(Topic, id=topic_id)
		topic.approved = True
		topic.save()

		data['status'] = 'ok'
		return Response(data)


class DisApproveTopicAPI(APIView):

	permission_classes = [IsAdminUser]

	def delete(self, request):

		topic_id: int = request.POST.get('id_of_topic', None)
		data: dict = {}
		topic = get_object_or_404(Topic, id=topic_id)
		topic.delete()
		return Response(data)
