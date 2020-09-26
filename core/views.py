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

    # get user
    u = message.from_user
    user = None
    try:
        user = User.objects.get(id=u.id)
    except Exception as err:
        print("user object not found: ", err)
        try:
            # save user
            user = User.objects.create(id=u.id, is_bot=u.is_bot, first_name=u.first_name, username=u.username, last_name=u.last_name, language_code=u.language_code)
        except Exception as err:
            print("object creation error: ", err)

    # save message
    if user != None:
        location = None
        if message.location != None:
            location = Location.objects.create(latitude=message.location.latitude, longitude=message.location.longitude)
        date = datetime.datetime.fromtimestamp(message.date)
        Message.objects.create(message_id=message.message_id, from_user=user, date=date, text=message.text, location=location)

    # send echo
    bot.send_message(chat_id=message.chat.id, text=message.text)


@csrf_exempt
@require_POST
def pull_messages(request):
    print("pull_messages")
    print(request.body.decode("utf-8"))
    updates = Update.de_json(request.body.decode("utf-8"))
    bot.process_new_updates([updates])
    return HttpResponse(status=200)


def get_last_message(request):
    message_text = None
    try:
        all_messages = Message.objects.all()
        last_message = all_messages[len(all_messages)-1]
        if last_message != None:
            message_text = str(last_message) + (str(last_message.location) if last_message.location != None else "")
    except Exception as err:
        print("couldn't get last message: ", err)
    return render(request, "view_message.html", {'message':message_text})


def get_all_messages(request):
    message_text_cat = ""
    try:
        for message in Message.objects.all():
            if message != None:
                message_n = str(message) + "\n"
                message_text_cat += message_n
    except Exception as err:
        print("couldn't get messages: ", err)
    return render(request, "view_message.html", {'message':message_text_cat})


#def acme_challenge(request):
#    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)
