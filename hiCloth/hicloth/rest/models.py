from django.db.models import *
from django.contrib.auth.models import User


class HiClothUser(Model):
    user = OneToOneField(User)
    phoneNumber = CharField(max_length=20)
    # :D


class Tag(Model):
    name = CharField(max_length=200, default="none")


class TagRelationship(Model):
    firstTag = ForeignKey(Tag, related_name="firstTag")
    secondTag = ForeignKey(Tag, related_name="secondTag")
    relType = CharField(max_length=200)


class Image(Model):
    URL = URLField(max_length=500)  # in site => 'WTF.com/image.jpg'
    location = CharField(max_length=500)  # in local machine => '/usr/bin/...'
    date = DateTimeField()
    tags = CharField(max_length=200)
    numberOfLikes = IntegerField(default=0)


class UserImageAction(Model):
    user = ForeignKey(User)
    image = ForeignKey(Image)
    date = DateTimeField(auto_now_add=True)
    actionType = SmallIntegerField()  # types:
                                      # 1   =>like
                                      # 999 =>share
                                      # -1  => dislike
                                      # ...


class UserTagLike(Model):
    tag = ForeignKey(Tag)
    user = ForeignKey(User)
    date = DateTimeField(auto_now_add=True)
    isUserLike = BooleanField(default=False)  # like=True, dislike=False
