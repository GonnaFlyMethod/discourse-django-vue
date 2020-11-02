from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.views import View
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CountriesSerializer, SignUpSerializer

from .models import Country


class SignUpFormView(APIView):

	temlate = 'accounts/sign_up.html'

	def get(self, request):

		if not request.user.is_authenticated:
			context = {
				'reg_user_url': reverse('accounts:sign-up'),
				'success_url': reverse('discourse:main')
			}
			return render(request, self.temlate, context)
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
			# return HttpResponseRedirect(reverse('discourse:main'))
			return Response(data)
		else:
			data = serializer.errors
			return Response(data)


class GetCountriesAPI(APIView):

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data)


class SignInView(APIView):

	template = 'accounts/sign_in.html'

	def get(self, request):

		if not request.user.is_authenticated:
			context = {
				'sign_in_url': reverse('accounts:sign-in')
			}
			return render(request, self.template, context)
		else:
			return HttpResponseBadRequest()

	def post(self, request):
		email_of_user = request.data['email']
		password = request.data['pasword']
		user = authenticate(email=email_of_user, password=password)

		data = {}
		if user is not None:
			if user.is_active:
				login(request, user)
				data['status'] = 'OK'
				return Response(data)
			else:
				data['status'] = 'banned'
		else:
			data['status'] = 'wrong_email_or_pass'
