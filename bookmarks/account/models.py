from django.db import models 
from django.conf import settings 

class Profile(models.Model): 
    #使用AUTH_USER_MODEL设置来引用这个用户模型
    user = models.OneToOneField(settings.AUTH_USER_MODEL) 
    date_of_birth = models.DateField(blank=True, null=True) 
    #photo字段是一个ImageField字段，需要安装Pillow：pip install Pillow
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True) 
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
