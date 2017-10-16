from django.db import models
from django.conf import settings

from django.utils.text import slugify
from django.core.urlresolvers import reverse
# Create your models here.


class Image(models.Model):
    #一个用户可以 post 多张图片， 但是每张图片只能由一个用户上传
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created')
    title = models.CharField(max_length=200)
    #一个只包含字母、数字、下划线、和连字符的标签， 用于创建优美的 搜索引擎友好（SEO-friendly）的 URL
    slug = models.SlugField(max_length=200,blank=True)
    #url ： 这张图片的源 URL
    url = models.URLField()
    #image ： 图片文件
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    # ForeignKey 字段或者带有 unique=True 的字段表明了一个索引的创建
    created = models.DateField(auto_now_add=True,db_index=True)
    #一个字段来保存喜欢这张图片的用户。我们需要一个多对多关系。
    #因为一个用户可能喜欢很多张图片，一张图片也可能被很多用户喜欢
    #ManyToMany 字段提供了一个多对多管理器,这个管理器使我们可以回溯相关联的对象比如： 
    #image.user_like.all() 或者从一个 user 中回溯，比如：user.images_liked.all()
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',blank=True)
    #使用信号功能
    #total_likes 字段给每张图片存储被用户喜欢的总数
    total_likes = models.PositiveIntegerField(db_index=True,default=0)
    def __str__(self):
        return self.title
    def save(self,*args,**kwargs):
        if not self.slug:
            #使用了 Django 提供的 slugify() 函数在没有提供 slug 
            #字段时根据给定的图片标题自动生 slug
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = "undefined"
        super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self): 
        return reverse('images:detail',args=(self.id,self.slug))
    
    class Meta:
        ordering = ('-created',)

















