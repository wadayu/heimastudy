from django.contrib import admin

from .models import HeroInfo,BookInfo

# Register your models here.


class BookInfoAdmin(admin.ModelAdmin):
    # fields = ('title','pub_data','reads','comments')
    list_display = ['title','pub_data','reads','comments']


class HeroInfoAdmin(admin.ModelAdmin):
    # fields = ('name','age','skill','book','add_time')
    list_display = ['name','age','skill','book','add_time']

admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
