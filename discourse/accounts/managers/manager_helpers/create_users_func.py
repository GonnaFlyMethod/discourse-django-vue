def create_acc(user_obj, arguments: dict, manager_obj, user="common_user"):
    """Depending on the value 'user' argument creates a certain type of user."""
    user_obj.first_name = arguments["first_name"]
    user_obj.second_name = arguments["second_name"]
    user_obj.sex = arguments["sex"]
    user_obj.country = arguments["country"]
    user_obj.date_of_birth = arguments["date_of_birth"]

    if user == "common_user":
        user_obj.is_active = True
        user_obj.is_staff = False
        user_obj.is_admin = False
        user_obj.is_superuser = False
    else:
        user_obj.is_active = True
        user_obj.is_staff = True
        user_obj.is_admin = True
        user_obj.is_superuser = True

    user_obj.set_password(arguments["password"])
    user_obj.save(using=manager_obj._db)
    return user_obj
