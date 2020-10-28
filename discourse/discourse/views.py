import re
import calendar

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
		print(data_to_display)
		return Response(data_to_display)