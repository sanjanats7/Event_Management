from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username","").strip()
        password = data.get("password","").strip()
        print(f"Attempting to register user: {username}")
        if not username or not password:
            return JsonResponse({"status": "failure", "message": "Username and password are required"})

        # if User.objects.filter(username__iexact=username).exists():
        #     return JsonResponse({"status": "failure", "message": "Username already exists"})

        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        return JsonResponse({"status": "success", "message": "User registered successfully"})
    return JsonResponse({"status": "failure", "message": "Invalid request method"})

@csrf_exempt

def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return JsonResponse({"status": "success", "message": "Login successful"})
            else:
                return JsonResponse({"status": "failure", "message": "Invalid password"})
        except User.DoesNotExist:
            return JsonResponse({"status": "failure", "message": "User not found"})
    return JsonResponse({"status": "failure", "message": "Invalid request method"})
# Create your views here.
