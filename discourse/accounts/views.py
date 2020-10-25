from django.shortcuts import render

from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CountriesSerializer

from .models import Country


class SignUpFormView(View):

	def get(self, request):
		temlate = 'accounts/sign_up.html'
		return render(request, temlate)


class GetCountriesAPI(APIView):

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountriesSerializer(countries, many=True)
        return Response(serializer.data)

