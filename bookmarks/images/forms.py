from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title','url','description')
        #���ǵ��û������ڱ���ֱ��ΪͼƬ��� URL
        #���ǽ���ʹ��һ�� JavaScropt ��������������վ��ѡ��һ��ͼƬȻ�����ǵ�
        #�������Բ�������ʽ��������ͼƬ�� URL
        #���Ǹ�д url �ֶε�Ĭ�Ͽؼ���widget��Ϊһ�� HiddenInput �ؼ�������ؼ���
        #�ᱻ��ȾΪ������ type="hidden" �� HTML Ԫ��
        #������ؼ�����Ϊ���ǲ������û���������ֶ�
        widgets={
            'url':forms.HiddenInput,
        }
    #ͨ��ʹ���� clean_<fieldname> ��ʽ
    #�����ķ�����ʵ�֡��������������Ϊһ����ʵ��ִ�� is_valid() ʱִ��
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given url does not match valid image extensions')
        return url
    #ModelForm �ṩ��һ�� save() ����������Ŀǰ��ģ��ʵ�������ݿ��У����ҷ���һ������
    #��� commit �� False �� save() �������᷵��һ��ģ��ʵ�����ǲ������������󱣴浽���ݿ���
    def save(self, force_insert=False,force_update=False,commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),image_url.rsplit('.', 1)[1].lower())
        # �Ӹ����� URL ������ͼƬ
        response = request.urlopen(image_url)
        #ʹ�� Python �� urllib ģ��������ͼƬ��Ȼ����� save() ������ͼƬ���ݸ�һ��
        #ContentFiel ��������������ص��ļ���ʵ����
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image















