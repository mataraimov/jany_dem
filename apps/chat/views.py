from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.safestring import mark_safe
from .forms import MessageForm
from .models import Message, Chat
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def chat_list(request):
    chats = Chat.objects.filter(users=request.user)
    for chat in chats:
        recipient = chat.other_user(request.user).username  # access the recipient object
        print(recipient)
    return render(request, 'chat_list.html', {'chat_list': chats})


def ws_chat(request, room_name):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()

    context = {'room_name': room_name}
    return render(request, 'chat_room.html', context)


def send_chat_message(event):
    message = event['message']
    room_name = event['room_name']

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        room_name,
        {
            'type': 'chat_message',
            'message': message,
        }
    )


@login_required
def chat_room(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    if request.user != recipient:
        chats = Chat.objects.filter(users=request.user)
        print(mark_safe(recipient_username))
        chat = Chat.objects.filter(users=request.user).filter(users=recipient).first()
        if not chat:
            chat = Chat.objects.create()
            chat.users.add(request.user, recipient)
            chat.recipient = recipient # add this line
            chat.save()
        messages = Message.objects.filter(
            sender=request.user,
            chat=chat
        ) | Message.objects.filter(
            sender=recipient,
            chat=chat
        )
        return render(request, 'chat_room.html', {
            'recipient_username': mark_safe(recipient_username),
            'messages': messages,
            'ws_server_path': reverse('ws_chat', args=[recipient_username]),
        })
    else:
        return HttpResponseBadRequest()


from django.db.models import Count

@login_required
def send_message(request, recipient_username):
    recipient = get_object_or_404(User, username=recipient_username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            chat = Chat.objects.filter(users__in=[request.user, recipient]).annotate(num_users=Count('users')).filter(num_users=2).first()
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.chat = chat
            message.sent_at = timezone.now()
            message.save()
            return redirect('chat_room', recipient_username=recipient_username)
    else:
        form = MessageForm()
    return render(request, 'chat_room.html', {'form': form, 'recipient_username': recipient_username})



# @login_required
# def chat_room(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     messages = Message.objects.filter(
#         sender=request.user,
#         recipient=recipient
#     ) | Message.objects.filter(
#         sender=recipient,
#         recipient=request.user
#     )
#     return render(request, 'chat_room.html', {
#         'recipient_username': mark_safe(recipient_username),
#         'messages': messages,
#         'ws_server_path': reverse('ws_chat', args=[recipient_username]),
#     })


# @login_required
# def send_message(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.sent_at = timezone.now()
#             message.save()
#             return redirect('chat_room', recipient_username=recipient_username)
#     else:
#         form = MessageForm()
#     return render(request, 'chat_room.html', {'form': form, 'recipient_username': recipient_username})

# @login_required
# def chat(request, username):
#     recipient = User.objects.get(username=username)
#     messages = Message.objects.filter(sender=request.user, recipient=recipient) | Message.objects.filter(sender=recipient, recipient=request.user)
#     messages = messages.order_by('timestamp')
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.save()
#             return redirect('chat', username=username)
#     else:
#         form = MessageForm()
#     return render(request, 'chat.html', {'recipient': recipient, 'messages': messages, 'form': form})

# @login_required
# def send_message(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.sent_at = timezone.now()
#             message.save()
#             return redirect(reverse('chat_room', args=[recipient_username]))
#         else:
#             # Print the errors to see what's wrong with the form validation
#             print(form.errors)
#             return HttpResponseBadRequest("Invalid form")
#     else:
#         form = MessageForm()
#     return render(request, 'send_message.html', {'form': form})


# @login_required
# def send_message(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = request.user
#             message.recipient = recipient
#             message.sent_at = timezone.now()
#             message.save()
#             return redirect(reverse('chat_room', args=[recipient_username]))
#         else:
#             return HttpResponseBadRequest("Invalid form")
#     else:
#         form = MessageForm()
#     return render(request, 'send_message.html', {'form': form})

# @login_required
# def chat_room(request, recipient_username):
#     recipient = get_object_or_404(User, username=recipient_username)
#     messages = Message.objects.filter(
#         sender=request.user,
#         recipient=recipient
#     ) | Message.objects.filter(
#         sender=recipient,
#         recipient=request.user
#     )
#     return render(request, 'chat_room.html', {
#         'recipient_username': mark_safe(recipient_username),
#         'messages': messages,
#         'ws_server_path': reverse('ws_chat'),
#     })