import pprint

from django.shortcuts import render

from django.contrib.auth import authenticate, login, views
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.views import View

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from discourse.models import Topic

from .serializers import CountriesSerializer, SignUpSerializer, UserSerializer

from .models import Country, Account


class SignUpFormView(APIView):
	permission_classes = [AllowAny]
	template = 'accounts/sign_up.html'

	def get(self, request):

		if not request.user.is_authenticated:
			context = {
				'reg_user_url': reverse('accounts:sign-up'),
				'success_url': reverse('discourse:main')
			}
			return render(request, self.template, context)
		else:
			return HttpResponseBadRequest()

	def post(self, request):
		data = request.data
		_mutable = request.data._mutable
		request.data._mutable = True
		if request.data['country']:
			country_id = Country.objects.get(name=request.data['country']).id			
			data['country'] = country_id
		else:
			data['country'] = ''

		request.data._mutable = _mutable
		
		serializer = SignUpSerializer(data=data)

		data = {}
		if serializer.is_valid():
			account = serializer.save()
			new_user = authenticate(email=serializer.validated_data['email'],
								password=serializer.validated_data['password'])
			login(request, new_user)
			data['status'] = 'OK'
			return Response(data)
		else:
			data = serializer.errors
			return Response(data)


class GetCountriesAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data)


class SignInView(APIView):
	permission_classes = [AllowAny]

	template = 'accounts/sign_in.html'

	def get(self, request):

		if not request.user.is_authenticated:
			context = {
				'sign_in_url': reverse('accounts:sign-in'),
				'success_url': reverse('discourse:main')
			}
			return render(request, self.template, context)
		else:
			return HttpResponseBadRequest()

	def post(self, request):
		email_of_user = request.data['email']
		password = request.data['password']
		user = authenticate(email=email_of_user, password=password)
		data = {}
		if user is not None:
			if user.is_active:
				login(request, user)
				data['status'] = 'OK'
			# Banned
			else:
				data['status'] = 'wrong_email_or_pass'
		else:
			data['status'] = 'wrong_email_or_pass'
		return Response(data)


class LogoutView(views.LogoutView):
    """Log out for an user."""
    template_name = 'accounts/logout.html'


# User profile

class UserProfileView(View):
	template = 'accounts/user_profile.html'
	def get(self, request, user_id):

		context = {
			'user_profile_data_api': reverse('accounts:user-profile-api',
				                             kwargs={'user_id':user_id}),
		}
		return render(request, self.template, context)


class UserProfileAPI(APIView):
	permission_classes = [IsAuthenticatedOrReadOnly]

	def get(self, request, user_id):
		usr = Account.objects.get(id=user_id)
		serializer = UserSerializer(usr)

		final_resp = serializer.data
		for topic in final_resp['topics_created']:
			
			topic_id = Topic.objects.get(id=topic['id']).id
			topic['topic_url'] = reverse('discourse:topic-detail',
				                         kwargs={'topicID':topic_id,
				                                 'type_': 'get'})

		return Response(final_resp)
