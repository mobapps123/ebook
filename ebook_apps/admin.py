from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(BookCategory)
admin.site.register(User)
admin.site.register(Books)
admin.site.register(ContactUs)
admin.site.register(BookInvitation)
admin.site.register(Notifications)

admin.site.register(Subscription)