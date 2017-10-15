from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

#ʹ�� receiver() װ������ users_like_changed ����ע���һ�� receiver ����
#Ȼ�����ǽ��ú������Ӹ� m2m_changed �źţ�������������� Image.users_like.through ����
#�����������ֻ�е� m2m_changed �źű� Image.users_like.through ִ�е�ʱ��ű�����
@receiver(m2m_changed, sender=Image.user_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.user_like.count()
    instance.save()
















