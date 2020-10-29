from django import forms
from django.contrib.auth.forms import UserCreationForm
                                       
# Current app module.
from .models import Account 


class CreateUser(UserCreationForm):
    """Form for creating user account in the system."""
    class Meta:
        model = Account

        first_name = forms.CharField(max_length=50,
                                     widget= forms.TextInput
                                     (attrs={'type':'text',
                                             'name':'first_name',
                                             'class': 'form-control my-input',
                                             'id': 'first_name',
                                             'placeholder': 'First name'}))

        second_name = forms.CharField(max_length=50,
                                     widget= forms.TextInput
                                     (attrs={'type':'text',
                                             'name':'second_name',
                                             'class': 'form-control my-input',
                                             'id': 'second_name',
                                             'placeholder': 'Second name'}))
        email = forms.EmailField(max_length=300,
                                       widget= forms.TextInput
                                       (attrs={'type':'email',
                                               'name':'second_name',
                                               'class': 'form-control my-input',
                                               'id': 'email',
                                               'placeholder': 'Second name'}))

        fields = ['first_name', 'second_name', 'email', 'sex', 'date_of_birth',
                  'country',
                  ]

        help_texts = {
            "first_name": "Enter your real First name",
            "second_name": "Enter your real Second name",
            "email": "Enter your email",
            "sex": "Select your sex",
            "date_of_birth": "Enter your date of birth",
            "country": "Select your country from the list",
        }

    def clean(self, *args, **kwargs):
        """Compare first_name and second_name fields in form, checks that their
        value is not the same."""
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        second_name = cleaned_data.get('second_name')

        if first_name == second_name:
            raise forms.ValidationError("First name and Second name must be " +
                                        "different!")
        return cleaned_data

    def clean_first_name(self, *args, **kwargs):
        """Checks that first_name field doesn't contain digits and field's
        length is not over 15 characters."""
        first_name = self.cleaned_data.get('first_name')

        for i in first_name:
            if i.isdigit():
                raise forms.ValidationError("The First name cannot contain" +
                                            "numbers")

        if len(first_name) <= 15:
            return first_name
        else:
            raise forms.ValidationError("This is not a valid First Name!")

    def clean_second_name(self, *args, **kwargs):
        """Checks that second_name field doesn't contain digits and field's
        length is not over 15 characters."""
        second_name = self.cleaned_data.get('second_name')

        for i in second_name:
            if i.isdigit():
                raise forms.ValidationError("The Second name cannot contain" +
                                            "numbers")

        if len(second_name) <= 15:
            return second_name
        else:
            raise forms.ValidationError("This is not a valid Second Name!")
