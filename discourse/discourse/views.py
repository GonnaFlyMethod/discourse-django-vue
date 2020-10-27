from django.views import View
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TopicsSerializer, CommentToTopicSerializer

from .models import Topic


class MainPageView(View):

	def get(self, request):
		return render(request, 'discourse/main.html')


class GetTopicsApi(APIView):

	def get(self, request):
		get_all_topics = Topic.objects.all()
		serializer = TopicsSerializer(get_all_topics, many=True)

		return Response(serializer.data)