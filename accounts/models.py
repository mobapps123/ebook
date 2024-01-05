from django.db import models

# Create your models here.

class Home(models.Model):
    heading = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)
    youtube_link = models.URLField(null=True,blank=True)

class HowDoesebooks(models.Model):
    top_heading = models.CharField(max_length=255,null=True,blank=True)
    heading = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)
   

class EBookExperience(models.Model):
    heading = models.CharField(max_length=100,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    image1 = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    sub_title = models.CharField(max_length=100,null=True,blank=True)
    icon = models.FileField(null=True,blank=True)




class OurServices(models.Model):
    background_image = models.FileField(null=True,blank=True)
    top_heading = models.CharField(max_length=200,null=True,blank=True)
    heading = models.CharField(max_length=200,null=True,blank=True)
    icon = models.CharField(max_length=100,null=True,blank=True)
    sub_heading = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)


class OurPartner(models.Model):
    image = models.FileField(null=True,blank=True)


class StudioExperience(models.Model):
    heading = models.CharField(max_length=100,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    image1 = models.ImageField(null=True,blank=True)
    image2 = models.ImageField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    icon_title = models.CharField(max_length=100,null=True,blank=True)
    icon = models.FileField(null=True,blank=True)



class LearnEverything(models.Model):
    heading = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)




class Footer(models.Model):
    logo = models.FileField(null=True,blank=True)
    facebook = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    twitter = models.URLField(null=True,blank=True)
    linkedin = models.URLField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)


class RequestDemo(models.Model):
    email = models.EmailField(null=True,blank=True)


class TermsCondition(models.Model):
    image = models.FileField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)

class PrivacyPolicy(models.Model):
    image = models.FileField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)


class CookiePolicy(models.Model):
    image = models.FileField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)


class Faq(models.Model):
    heading = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(null=True,blank=True)
    question = models.CharField(max_length=255,null=True,blank=True)
    ans = models.TextField(null=True,blank=True)


