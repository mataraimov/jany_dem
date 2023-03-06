from django import template

register = template.Library()

@register.filter
def other_user(chat, user):
    return chat.other_user(user)
