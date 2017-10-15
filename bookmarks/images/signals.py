from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

#使用 receiver() 装饰器将 users_like_changed 函数注册成一个 receiver 函数
#然后我们将该函数附加给 m2m_changed 信号，并将这个函数与 Image.users_like.through 连接
#这样这个函数只有当 m2m_changed 信号被 Image.users_like.through 执行的时候才被调用
@receiver(m2m_changed, sender=Image.user_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.user_like.count()
    instance.save()
















