from django.shortcuts import render
import telebot
from telebot.types import Update
from getplacebot import settings
from core.models import Message, User, Location
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime


bot = telebot.TeleBot(settings.TELEBOT_API_TOKEN)
bot.set_webhook(url=settings.WEBHOOK_URL)

@bot.message_handler()
def handle_message(message):
    print("got message")
    u = message.from_user
    print("USER")
    print("****************")
    print(u)
    print("****************")
    user = None
    try:
        user = User.objects.get(id=u.id)
    except Exception as err:
        print("user object not found: ", err)
        try:
            user = User.objects.create(id=u.id, is_bot=u.is_bot, first_name=u.first_name, username=u.username, last_name=u.last_name, language_code=u.language_code)
            location = None
            if message.location != None:
                location = Location.objects.create(latitude=message.location.latitude, longitude=message.location.longitude)
            date = datetime.datetime.fromtimestamp(message.date)
            message = Message.objects.create(message_id=message.message_id, from_user=user, date=date, text=message.text, location=location)
        except Exception as err:
            print("object creation error: ", err)
    bot.send_message(chat_id=message.chat.id, text=message.text)


@csrf_exempt
@require_POST
def pull_messages(request):
    print("pull_messages")
    updates = Update.de_json(request.body.decode("utf-8"))
    bot.process_new_updates([updates])
    return HttpResponse(status=200)


def get_last_message(request):
    message_text = None
    try:
        message_text = str(Message.objects.all()[-1])
    except:
        print("couldn't get last message")
    return render(request, "view_message.html", {'message':message_text})


def get_all_messages(request):
    message_text_cat = None
    try:
        for message in Message.objects.all():
            message_text_cat += str(message) + "\n"
    except:
        print("couldn't get messages")
    return render(request, "view_message.html", {'message':message_text_cat})


#def acme_challenge(request):
#    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)
