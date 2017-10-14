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



from django.contrib.auth.models import User 

class Contact(models.Model): 
    user_from = models.ForeignKey(User, related_name='rel_from_set') 
    user_to = models.ForeignKey(User, related_name='rel_to_set') 
    created = models.DateTimeField(auto_now_add=True, db_index=True) 
    class Meta: 
        ordering = ('-created',) 
    def __str__(self): 
        return '{} follows {}'.format(self.user_from, self.user_to)

# Add following field to User dynamically User.add_to_class('following',
#使用Django模型（models）的add_to_class()方法给User模型（model）添加monkey-patch
#在运行时对已有的代码进行修改，而不需要修改原始代码
#symmetrical=Flase来定义一个非对称（non-symmetric）关系。这表示如果我关注了你，你不会自动的关注我
User.add_to_class('following',
    models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))

#当你使用了一个中介模型（intermediate model）给多对多关系，一些关系管理器的方法将不可用，
#例如：add()，create()以及remove()。你需要创建或删除中介模型（intermediate model）的实例来代替










