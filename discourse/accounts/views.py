from django.shortcuts import render

from django.http import JsonResponse
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
		return render(request, self.temlate)

	def post(self, request):
		serializer = SignUpSerializer(data=request.data)

		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'OK'
		else:
			data = serializer.errors
		return JsonResponse(data)


class GetCountriesAPI(APIView):

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data)
