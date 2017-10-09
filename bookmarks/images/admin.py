from django.contrib import admin
from .models import Image
# Register your models here.

#在浏览器中打开 http://127.0.0.1:8000/admin/ ,可以看到 Image 模型已经注册到了管理站点中
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','slug','image','created']
    list_filter = ['created']
    
admin.site.register(Image,ImageAdmin)



