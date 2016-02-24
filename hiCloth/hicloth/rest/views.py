# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
from models import Image, UserImageAction, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from operator import __or__ as OR
from rest_framework.authtoken.models import Token
from django.core.exceptions import *
from django.utils import timezone
from django.conf import settings


def getImages(request):
    response = []
    numberOfImages = int(request.REQUEST.get('viewSize', 20))
    indexOfPreviousImage = int(
        request.REQUEST.get('previousID', 0))

    indexOfStartImage = indexOfPreviousImage

    finalList = getListOfTags(request.REQUEST.get('tags', []))
    if request.REQUEST.get('isMostPopular', False):
        finalList = finalList.order_by('-numberOfLikes')
    try:
        isUserLike = int(request.REQUEST.get('isUserLiked', 0))
    except ValueError:
        isUserLike = 0
    if isUserLike and isUserAuthenticated(request):
        print isUserLike
        finalList = finalList.filter(userimageaction__user=getUser(request),
                                     userimageaction__actionType=1)
    startIndex = 0
    if not indexOfPreviousImage:
        finalList = finalList.order_by('-date')
    else:
        try:
            startIndex = list(finalList).index(finalList.get(pk=indexOfStartImage))
        except:
            pass

    for image in finalList[
            startIndex:startIndex + numberOfImages]:
        response.append({
            "tags": image.tags.split(","),
            "URL": settings.SERVER_IP_PORT + "static/rest/" + image.location,
            "ID": image.id,
            "isLiked": False if not isUserAuthenticated(request) else
            bool(UserImageAction.objects.filter(user=getUser(request),
                                                image=image,
                                                actionType=1)),
            "likeCount": image.numberOfLikes
        })
    return HttpResponse(json.dumps({
        "images": response,
        "numberOfImages": finalList.count()
    }), content_type='application.json')


def getAllOfTags(request):
    return HttpResponse(json.dumps({
        "tags": [tag.name for tag in Tag.objects.all()]
    }), content_type='application.json')


def getListOfTags(tags=None):
    if tags:
        listOfQueries = [Q(tags__contains=tag) for tag in tags.split(',')]

        print [tag for tag in tags.split('-')]
        return Image.objects.filter(reduce(OR, listOfQueries))

    return Image.objects.all()  # return all of tags if tags is empty


def getUser(request):
    try:
        return Token.objects.get(key=request.META.get('HTTP_AUTHORIZATION')).user
    except ObjectDoesNotExist:
        return 0


def createOrUpdateNewAction(request, imageID, actionType):
    print actionType, type(actionType)
    try:
        if actionType != 999:
            actionDoneBefore = UserImageAction.objects.filter(
                user=getUser(request),
                image_id=imageID
            ).exclude(actionType=999)[0]
            imageObject = Image.objects.get(pk=imageID)
            if actionDoneBefore.actionType < actionType:
                imageObject.numberOfLikes += 1
            elif actionDoneBefore.actionType > actionType:
                imageObject.numberOfLikes -= 1
            imageObject.save()
            actionDoneBefore.actionType = actionType
            actionDoneBefore.date = timezone.now()
            actionDoneBefore.save()

        else:
            UserImageAction.objects.create(user=getUser(request),
                                           image_id=imageID,
                                           actionType=actionType)
    except IndexError:
        if actionType == -1:
                return
        else:
            UserImageAction.objects.create(user=getUser(request),
                                           image_id=imageID,
                                           actionType=actionType)
            imageObject = Image.objects.get(pk=imageID)
            imageObject.numberOfLikes += int(actionType)
            imageObject.save()


def doAction(request):
    response = HttpResponse()
    messageToShow = "شما وارد سایت نشدید !!"
    statusCode = 200
    actions = {"like": 1, "dislike": -1, "share": 999}
    if isUserAuthenticated(request):
        try:
            #  default action is 'like'
            actionType = request.REQUEST.get('actionType', 'like').lower()
            imageID = int(request.REQUEST.get('imageID', 0))
            if imageID <= 0:
                raise ValueError("invalid image ID")
            createOrUpdateNewAction(request, imageID, actions[actionType])

            messageToShow = "action done :D"
        except(ObjectDoesNotExist, ValueError, KeyError) as error:
            messageToShow, response.status_code = str(error), 401
        except SyntaxError:
            messageToShow, response.status_code = u"لطفا عین آدم جیسون بفرستید", 401
    response.content, response.status_code = messageToShow, statusCode

    return HttpResponse(json.dumps({
        "message": response.content
    }), content_type='application.json')


def isUserAuthenticated(request):
    try:
        _ = Token.objects.get(
            key=request.META.get('HTTP_AUTHORIZATION')).user.id
        return True
    except ObjectDoesNotExist:
        return False