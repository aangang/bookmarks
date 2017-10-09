from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        #我们的用户不会在表单中直接为图片添加 URL
        #他们将会使用一个 JavaScropt 工具来从其他网站中选择一张图片然后我们的
        #表单将会以参数的形式接收这张图片的 URL
        #我们覆写 url 字段的默认控件（widget）为一个 HiddenInput 控件，这个控件将
        #会被渲染为属性是 type="hidden" 的 HTML 元素
        #用这个控件是因为我们不想让用户看见这个字段
        widgets={
            'url':forms.HiddenInput,
        }
    #通过使用以 clean_<fieldname> 形式
    #命名的方法来实现。这个方法会在你为一个表单实例执行 is_valid() 时执行
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extensions')
        return url
    #ModelForm 提供了一个 save() 方法来保存目前的模型实例到数据库中，并且返回一个对象
    #如果 commit 是 False ， save() 方法将会返回一个模型实例但是并不会把这个对象保存到数据库中
    def save(self, force_insert=False,force_update=False,commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.', 1)[1].lower())
        # 从给定的 URL 中下载图片
        response = request.urlopen(image_url)
        #使用 Python 的 urllib 模块来下载图片，然后调用 save() 方法把图片传递给一个
        #ContentFiel 对象，这个对象被下载的文件所实例化
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image















