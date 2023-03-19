from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Meep

 
# Register your models here.

#   Unregister Groups
admin.site.unregister(Group)

# Mix profile into User info
class ProfileInline(admin.StackedInline):
    model=Profile

#   Extend User Model
class UserAdmin(admin.ModelAdmin):
    model = User
    #just display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
#admin.site.register(Profile)

admin.site.register(Meep)