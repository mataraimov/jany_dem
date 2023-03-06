from django import template

from apps.chat.models import Chat

register = template.Library()
@register.filter(name='other_user_username')
def other_user_username(chat, user):
    other_user = chat.other_user(user)
    if other_user:
        return other_user.username
    return ''
