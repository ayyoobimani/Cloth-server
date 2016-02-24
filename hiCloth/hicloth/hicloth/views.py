# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest.models import *
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import re
from django.db import IntegrityError
import ast


@csrf_exempt
def registerProcess(request):
    response = HttpResponse(content_type='application.json')
    response.content = json.dumps({"message": "OK"})
    try:
        if request.method != "POST":
            raise RequestException("request must be POST !!")
        print ast.literal_eval(request.body).get('username')
        usernameOrPhone = ast.literal_eval(request.body).get('username')
        password = ast.literal_eval(request.body).get('password')
        passwordRepeat = ast.literal_eval(request.body).get('passwordRepeat')
        print usernameOrPhone, password, passwordRepeat
        if not usernameOrPhone:
            raise UserNameException(u"نام کاربری نمیتواند خالی باشد")
        if not (password and passwordRepeat):
            raise PasswordException(u"پسورد یا تکرار پسورد نمیتواند خالی باشد")
        if not (password == passwordRepeat):
            raise PasswordException(u"پسورد و تکرار پسورد باید یکسان باشد")
        newUser = User.objects.create_user(username=usernameOrPhone,
                                           password=password)
        newUser.save()
        newHiClothUser = HiClothUser(
            user=newUser,
        )
        authToken = Token.objects.create(user=newUser)
        response["authorization"] = authToken.key
        if isUserNameFieldPhone(usernameOrPhone):
            newHiClothUser.phoneNumber = usernameOrPhone
        newHiClothUser.save()
    except (UserNameException, PasswordException, RequestException) as err:
        response.content = json.dumps({
            "message": err.message
        })
    except IntegrityError:
        response.content = json.dumps({
            "message": u"نام کابری قبلا ثبت شده است"
        })
    except SyntaxError:
        response.content = json.dumps({
            u"لطفا عین آدم جیسون بفرستید :)"
        })
    return response


@csrf_exempt
def loginProcess(request):
    response = HttpResponse(content_type='application.json')
    messageToShow = "OK"
    try:
        if request.method != "POST":
            raise RequestException("request must be POST !!")
        username = ast.literal_eval(request.body).get('username')
        password = ast.literal_eval(request.body).get('password')
        print username, password
        user = authenticate(username=username, password=password)
        print bool(user)
        if user:
            token, isCreated = Token.objects.get_or_create(user=user)
            response["authorization"] = token.key
        else:
            messageToShow = u"نام کاربری یا رمز عبور اشتباه است"

    except (UserNameException, PasswordException, RequestException) as err:
        messageToShow = err.message
    except SyntaxError:
        messageToShow = "لطفا عین آدم جیسون بفرستید :)"
    response.content = json.dumps({
        "message": messageToShow
    })
    return response


def isUserNameFieldPhone(username):
    if re.match('0?9[1-3][0-9]{8}', username):
        return True
    return False


def LogoutView(request):
    response = {"status": "OK"}
    if isUserAuthenticated(request):
        Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).delete()
    return HttpResponse(json.dumps(response), content_type='application.json')


def UserView(request):
    response = {"username": "", "id": 0}
    if isUserAuthenticated(request):
        requestedUser = User.objects.get(pk=
                Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user.id)
        response["username"] = requestedUser.username
        response["id"] = requestedUser.pk
    return HttpResponse(json.dumps(response), content_type='application.json')


def isUserAuthenticated(request):
    try:
        _ = Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user.id
        return True
    except ObjectDoesNotExist:
        return False


class UserNameException(Exception):
    pass


class PasswordException(Exception):
    pass


class RequestException(Exception):
    pass