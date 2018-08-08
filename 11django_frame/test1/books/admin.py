from django.contrib import admin

from .models import HeroInfo,BookInfo,AreaInfo,UploadPic,Tinymce

# Register your models here.
class AreaInfoInline(admin.StackedInline):
    model = AreaInfo
    extra = 0

class BookInfoAdmin(admin.ModelAdmin):
    # fields = ('title','pub_data','reads','comments')
    list_display = ['title','pub_data','reads','comments']


class HeroInfoAdmin(admin.ModelAdmin):
    # fields = ('name','age','skill','book','add_time')
    list_display = ['name','age','skill','book','add_time']

class AreaInfoAdmin(admin.ModelAdmin):
    list_per_page = 10  # 每页展示的行数
    list_display = ['id','atitle','parent']  # 展示的列
    # list_filter = ['atitle'] # 需要创建过滤的列
    search_fields = ['atitle'] # 需要创建搜索的列
    fields = ['pid','atitle'] # 排列顺序
    actions_on_top = False    # 删除动作不让在顶部显示
    actions_on_bottom = True  # 删除动作在底部显示
    inlines = [AreaInfoInline]
    readonly_fields = ['id','atitle','pid']  # 只读

class UploadPicAdmin(admin.ModelAdmin):
    list_display = ['path']

admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AreaInfo,AreaInfoAdmin)
admin.site.register(UploadPic,UploadPicAdmin)
admin.site.register(Tinymce)

