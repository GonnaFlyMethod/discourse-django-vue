from rest_framework import serializers

from .models import Country, Account


class CountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['name',]


class SignUpSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'},
		                              write_only=True)

	class Meta:
		model = Account
		fields = ['first_name', 'second_name', 'email', 'date_of_birth', 'sex',
		          'country', 'password', 'password2']
		extra_kwargs = {
			'password':{'write_only':True}
		}

	def save(self):
		first_name = self.validated_data['first_name']
		second_name = self.validated_data['second_name']
		email = self.validated_data['email']
		date_of_birth = self.validated_data['date_of_birth']
		sex = self.validated_data['sex']
		country = self.validated_data['country']
		account = Account(
			              first_name=first_name,
			              second_name=second_name,
			              email=email,
			              date_of_birth=date_of_birth,
			              sex=sex,
			              country=country
        )
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			msg = {'password': 'Passwords must match'}
			raise serializers.ValidationError(msg)

		account.set_password(password)
		account.save()
		return account

