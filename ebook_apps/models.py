from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager





import datetime
import hashlib
import uuid
from typing import Any

import user_agents
from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _lazy
import hashlib

    

########## Custom Model manager ########
class CustomUserManager(BaseUserManager):
   def create_user(self, email, first_name,institute, last_name, phone_number, password):
         if not email:
            raise ValueError('The Email must be Set')
         if not first_name:
            raise ValueError("User Must have a first name")

         if not last_name:
            raise ValueError("User Must have a last name")

         user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            institute =institute,
           
         )
         user.set_password(password)
         user.save(using=self._db)
         return user

   
   def create_superuser(self,email,institute,first_name, phone_number, last_name, password):
         user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=password,
            institute=institute,

         )
         user.is_staff = True
         user.is_superuser = True
         user.is_admin = True
         user.is_organization = False
         user.is_student = False
         user.is_active  = True
         user.save(using=self._db)
         return user


############ Custom User Model ###########
class User(AbstractBaseUser):

   profile_pic = models.FileField(null=True,blank=True)
   email = models.EmailField(verbose_name = 'Email',max_length=255,unique=True)
   first_name = models.CharField(max_length=50,null=True,blank=True)
   last_name = models.CharField(max_length=50,null=True,blank=True)
   phone_number = models.CharField(max_length =15,null=True,blank=True, unique=True)
   address = models.CharField(max_length=100,null=True,blank=True)
   website = models.URLField(max_length=100,null=True,blank=True)
   is_active = models.BooleanField(default = False)
   is_admin = models.BooleanField(default = False)
   is_superuser = models.BooleanField(default = False)
   is_enduser = models.BooleanField(default=False)
   is_staff = models.BooleanField(default=False)
   is_student = models.BooleanField(default=False)
   is_organization = models.BooleanField(default=False)
   added_user = models.IntegerField(null=True,blank=True)
   institute = models.CharField(max_length=200,null=True,blank=True)
   created_at = models.DateTimeField(default=timezone.now)
   updated_at = models.DateTimeField(auto_now = True,null=True,blank=True)
   last_login = models.DateTimeField(null=True, blank=True)
   books = models.ManyToManyField('Books', blank=True)
   
   objects = CustomUserManager()
   USERNAME_FIELD = 'email'
   EMAIL_FIELD = 'email'
   REQUIRED_FIELDS = ['first_name','last_name',  'institute', 'phone_number']

   def __str__(self):
        return self.email

   def has_perm(self, perm, obj=None):
      return True  # You can customize this based on your needs

   def has_module_perms(self, app_label):
      return True  # You can customize this based on your needs

   def get_all_permissions(self, obj=None):
      return []  # You can customize this based on your needs



   class Meta:
      verbose_name = 'User'
      verbose_name_plural = 'Users'

class ManageLoginTime(models.Model):
   users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="manageLoginTime")
   login_start_time = models.TimeField(null=True,blank=True)
   login_end_time = models.TimeField(null=True, blank=True)
   institute = models.CharField(max_length=100, blank=True, null=True)


class UserVisit(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   browser_name = models.CharField(max_length=255, blank=True, null=True)
   visit_count = models.PositiveIntegerField(default=0)





class BookCategory(models.Model):
   book_category = models.CharField(max_length=100,null=True,blank=True)
   created_at=models.DateField(auto_now_add=True,null=True,blank=True)
   updated_at=models.DateField(auto_now=True,null=True,blank=True)
   



########### book models 
class Books(models.Model):
   category = models.ForeignKey(BookCategory,on_delete=models.CASCADE,null=True,blank=True)
   description = models.TextField(null=True,blank=True)
   title = models.CharField(max_length=255,null=True,blank=True)
   author = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   book_pdf = models.FileField(null=True,blank=True)
   price = models.FloatField(null=True,blank=True)
   publication_date = models.DateField(null=True,blank=True)
   added_by = models.IntegerField(null=True,blank=True)
   collection = models.BooleanField(null=True,blank=True)
   created_at=models.DateField(auto_now_add=True,null=True,blank=True)
   updated_at=models.DateField(auto_now=True,null=True,blank=True)
   is_active = models.BooleanField(default = True)
   total_pages = models.PositiveIntegerField(null=True,blank=True)
   is_organization = models.BooleanField(default=False)
   is_student = models.BooleanField(default=False)
   start_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   end_time = models.DateTimeField(null=True, blank=True)


class Subscription(models.Model):
   DURATION_CHOICES = [
      (3, '3 Months'),
      (6, '6 Months'),
      (12, '12 Months'),
   ]
   user = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have a User model
   start_date = models.DateField()
   duration_months = models.IntegerField(choices=DURATION_CHOICES,null=True,blank=True)
   expiration_reminder = models.BooleanField(default=False)
   @property
   def end_date(self):
        return self.start_date + relativedelta(months=self.duration_months)




class Recently_Viewed(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
   book = models.ForeignKey(Books, on_delete=models.CASCADE,null=True,blank=True)
   institute_name = models.CharField(max_length=100, null=True, blank=True, default="guest")
   created_at=models.DateField(auto_created=True,null=True,blank=True)
   updated_at=models.DateField(auto_created=True,null=True,blank=True)
   viewed_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)



class Favorite(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   fav_book = models.ForeignKey(Books, on_delete=models.CASCADE)


class BookVisit(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   books = models.ForeignKey(Books, on_delete=models.CASCADE)
   visit_count = models.PositiveIntegerField(default=0)
   start_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   end_time = models.DateTimeField(null=True, blank=True)
   completed = models.BooleanField(null=True, blank=True, default=False)
   institute_name = models.CharField(max_length=100, null=True, blank=True, default="guest")
   created_at=models.DateField(auto_created=True,null=True,blank=True)
   updated_at=models.DateField(auto_created=True,null=True,blank=True)
   def duration(self):
      return self.end_time - self.start_time


class Collections(models.Model):
   name = models.CharField(max_length=255,null=True,blank=True,unique=True)
   image = models.FileField(null=True,blank=True)
   books = models.ForeignKey(Books,on_delete=models.CASCADE,null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   updated_at=models.DateField(auto_now=True,null=True,blank=True)
   user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="corporate_collection",null=True,blank=True)




class CategoryVisit(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   book = models.ForeignKey(Books, on_delete=models.CASCADE)
   visit_count = models.PositiveIntegerField(default=0)
   created_at=models.DateField(auto_created=True,null=True,blank=True)
   updated_at=models.DateField(auto_created=True,null=True,blank=True)



class BookReadProgress(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   book = models.ForeignKey(Books, on_delete=models.CASCADE)
   last_read_page = models.PositiveIntegerField(default=0)
   read_count = models.PositiveIntegerField(default=0)


 

####### review models start here..
class Review(models.Model):
   star_rating = models.PositiveSmallIntegerField(choices=[(1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')],blank=True,null=True)
   def __str__(self):
        return f"{self.user} - {self.book} - {self.star_rating} stars"
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   book = models.ForeignKey(Books, on_delete=models.CASCADE) 
   text = models.TextField()
   rating = models.PositiveSmallIntegerField(default=5)
   created_at = models.DateTimeField(auto_now_add=True) 



class TotalVisit(models.Model):
   book_id = models.ForeignKey(Books,on_delete=models.CASCADE)
   user_id = models.ForeignKey(User,on_delete=models.CASCADE)


# class Like(models.Model):
#    user_id = 





class CollectionsList(models.Model):
   Collections_name = models.ForeignKey(Collections,on_delete=models.CASCADE,related_name='collection')
   books_id = models.ForeignKey(Books,on_delete=models.CASCADE)
   created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   updated_at=models.DateField(auto_now=True,null=True,blank=True)
   user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="corporate_collectionView",null=True,blank=True)


class Notifications(models.Model):
   receiver = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
   subject = models.CharField(max_length=100,null=True,blank=True)
   message = models.CharField(max_length=100)
   is_read = models.BooleanField(default=False)
   read_by = models.BooleanField(default=False)
   create_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
   def mark_as_read(self):
      self.is_read = True
      self.save()

class BookInvitation(models.Model):
   book = models.ForeignKey(Books, on_delete=models.CASCADE)
   invited_user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
   title = models.CharField(max_length=20,null=True,blank=True)
   is_read = models.BooleanField(default=False)
   read_by = models.BooleanField(default=False)
   create_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
   def mark_as_read(self):
      self.is_read = True
      self.save()


class ContactUs(models.Model):
   name = models.CharField(max_length=100,null=True,blank=True)
   company = models.CharField(max_length=100,null=True,blank=True)
   mobile_number = models.CharField(max_length=10,null=True,blank=True)
   business_email = models.EmailField(null=True,blank=True)
   subject = models.TextField(null=True,blank=True)
   message = models.TextField(null=True,blank=True)


class ContactBanner(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


class GetInTouch(models.Model):
   heading = models.CharField(max_length=255,null=True,blank=True)
   description = models.TextField(null=True,blank=True)
   address = models.CharField(max_length=200,null=True,blank=True)
   email = models.EmailField(max_length=255,null=True,blank=True)
   call  = models.CharField(max_length=15,null=True,blank=True)
   
   


########## about us models start here ##########
class AboutBanner(models.Model):
   heading = models.CharField(max_length=200,null=True,blank=True)
   banner_image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)



class TheFoundation(models.Model):
   top_heading = models.CharField(max_length=100,null=True,blank=True)
   heading = models.CharField(max_length=200,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)



class AboutTheBook(models.Model):
   heading = models.CharField(max_length=200,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


class Overview(models.Model):
   top_heading = models.CharField(max_length=200,null=True,blank=True)
   top_description = models.CharField(max_length=500,null=True,blank=True)
   heading = models.CharField(max_length=255,null=True,blank=True)
   description = models.TextField(null=True,blank=True)




############## blogs models #######
class BlogsBanner(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   banner_image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True) 



class BlogsDetails(models.Model):
   paragraph1 = models.TextField(null=True,blank=True)
   paragraph2 = models.TextField(null=True,blank=True)
   paragraph3 = models.TextField(null=True,blank=True)
   like = models.IntegerField(default=0, null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   date = models.IntegerField(null=True,blank=True)
   month = models.CharField(max_length=10,null=True,blank=True)
   title = models.CharField(max_length=255,null=True,blank=True)
   by_name = models.CharField(max_length=100,null=True,blank=True)
   description = models.TextField(null=True,blank=True)
   video = models.FileField(null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
   


class RequestADemo(models.Model):
   business_email = models.EmailField(verbose_name = 'Email',max_length=255,unique=True)
   first_name = models.CharField(max_length=50,null=True,blank=True)
   last_name = models.CharField(max_length=50,null=True,blank=True)
   message = models.TextField(null=True,blank=True)


########### digital publishing #####
class DigitalPubBanner(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   banner_image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True) 
   

######### Cater to Various 
class CaterToVarious(models.Model):
   heading = models.CharField(max_length=200,null=True,blank=True)
   title = models.CharField(max_length=255,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   description = models.TextField(null=True,blank=True)
   image = models.FileField(null=True,blank=True)


class MultiDevices(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   description = models.TextField(null=True,blank=True)
   image = models.ImageField(null=True,blank=True)
   icon = models.CharField(max_length=100,null=True,blank=True)
   small_heading = models.CharField(max_length=200,null=True,blank=True)
   small_description = models.TextField(null=True,blank=True)
   

class SecuredDistribution(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)



class Easilyintegrates(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True) 


class GetYourBranded(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)



####### ebooks store 
class BookStoreBanner(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   banner_image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True) 



class YourBrandedWebstore(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


class EasyIntegration(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


class FullyResponsive(models.Model):
   heading  = models.CharField(max_length=200,null=True,blank=True)
   image = models.ImageField(null=True,blank=True)
   description = models.TextField(null=True,blank=True) 

class SocialNetwork(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   span = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description1 = models.TextField(null=True,blank=True)
   description2 = models.TextField(null=True,blank=True)







########## ebook reader models start here 
class EbookReaderBanner(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


####### indybot models
class IndyBotBanner(models.Model):
   heading = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)

class Useprimary(models.Model):
   heading  = models.CharField(max_length=255,null=True,blank=True)
   image1 = models.FileField(null=True,blank=True)
   image2 = models.FileField(null=True,blank=True)
   image3 = models.FileField(null=True,blank=True)
   paragraph1 = models.TextField(null=True,blank=True)
   paragraph2 = models.TextField(null=True,blank=True)


class IndybotResponsive(models.Model):
   heading = models.CharField(max_length=200,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   description = models.TextField(null=True,blank=True)


class ReadYourBook(models.Model):
   top_heading = models.CharField(max_length=100,null=True,blank=True)
   title = models.CharField(max_length=100,null=True,blank=True)
   image = models.FileField(null=True,blank=True)
   heading = models.CharField(max_length=100,null=True,blank=True)
   description = models.TextField(null=True,blank=True)





class Staffmenu(models.Model):
   is_staff = models.BooleanField(default=False,null=True,blank=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
   dashboard = models.CharField(max_length=10,null=True,blank=True)
   details_book = models.CharField(max_length=10,null=True,blank=True)
   user_details = models.CharField(max_length=10,null=True,blank=True)
   manage_home = models.CharField(max_length=10,null=True,blank=True)
   manage_contact = models.CharField(max_length=10,null=True,blank=True)
   manage_category = models.CharField(max_length=50,null=True,blank=True)
   manage_collection = models.CharField(max_length=50,null=True,blank=True)
   digital_publishing = models.CharField(max_length=50,null=True,blank=True)
   ebook_store = models.CharField(max_length=50,null=True,blank=True)
   ebook_reader = models.CharField(max_length=50,null=True,blank=True)
   indybot = models.CharField(max_length=50,null=True,blank=True)
   notifications = models.CharField(max_length=50,null=True,blank=True)
   manage_cms = models.CharField(max_length=50,null=True,blank=True)
   manage_staff = models.CharField(max_length=50,null=True,blank=True)
   manage_blogs = models.CharField(max_length=50,null=True,blank=True)


class SurveyResponse(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
   question = models.CharField(max_length=50,null=True,blank=True)
   answer1 = models.CharField(max_length=50,null=True,blank=True)
   answer2 = models.CharField(max_length=50,null=True,blank=True)
   answer3 = models.CharField(max_length=50,null=True,blank=True)
   answer4 = models.CharField(max_length=50,null=True,blank=True)
   answer5 = models.CharField(max_length=50,null=True,blank=True)
   answer6 = models.CharField(max_length=50,null=True,blank=True)
   created_at = models.DateTimeField(auto_now_add=True,null=True)