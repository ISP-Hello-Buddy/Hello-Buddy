from django.contrib.auth.models import User

def new_user(username, password="Admin1234@",email="none@gmail.com") -> User:
    """Create a new Django user instance."""
    user = User.objects.create_user(username=username,password=password,email=email)
    user.save()
    return user