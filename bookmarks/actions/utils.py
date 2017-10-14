from django.contrib.contenttypes.models import ContentType
from .models import Action
import datetime
from django.utils import timezone


#定义一个快捷函数，该函数允许我们使用一种简单的方式创建新的 Action 对象
#有时候你的用户可能多次执行同个动作,会导致你停止存储和显示重复的动作,我们需要改善create_action() 函数来避免大部分的重复动作
def create_action(user, verb, target=None):
    # check for any similar action made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,verb= verb,created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,target_id=target.id)
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False

