# Django modules.
from django.contrib.auth.models import BaseUserManager

# !Triplinker modules:

# Current app modules.
from .manager_helpers.create_users_func import create_acc


class CustomAccountManager(BaseUserManager):
    """Creates common user and super user"""

    def create_user(self, first_name, second_name, email, sex,
                    date_of_birth, country, password, user_type="common_user"):
        user = self.model(
            email=self.normalize_email(email),
        )

        args = locals()
        class_instance = BaseUserManager()
        user_obj = create_acc(user, args, class_instance, user_type)
        return user_obj

    def create_superuser(self, first_name, second_name, email, sex,
                         date_of_birth, country, password):
        """Creates superuser on the base of the method 'create_user'."""
        user_obj = self.create_user(first_name, second_name, email, sex,
                                    date_of_birth, country, password,
                                    user_type="super_user")
        return user_obj
