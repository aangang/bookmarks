from django.db import models

from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.


class Action(models.Model):
    user = models.ForeignKey(User,related_name='actions',db_index=True)
    #这是用户执行操作的动作描述
    verb = models.CharField(max_length=255)
    #我们需要一个方法，可以让操作的 target（目标）对象
    #是任何一个已经存在的模型（model）的实例。这个场景就由 Django 内容类型框架
    #内容类型框架位于 django.contrib.contenttypes。这个应用可以跟踪你的项目中所有的模型
    #target_ct：一个 ForeignKey 字段指向 ContentType 模型（model）
    target_ct = models.ForeignKey(ContentType,blank=True,null=True,related_name='target_obj')
    #target_id：一个 PositiveIntegerField 用来存储被关联对象的 primary key
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    #target：一个 GenericForeignKey 字段指向被关联的对象基于前面两个字段的组合之上
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,db_index=True)
    class Meta:
        ordering = ('-created',)






