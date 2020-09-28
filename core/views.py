from django.shortcuts import render
import telebot
from telebot.types import Update
from getplacebot import settings
from core.models import User, Location, Photo, Bot
from core import constants
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import datetime


##########
# Init bot
##########

bot = telebot.TeleBot(settings.TELEBOT_API_TOKEN)
bot.set_webhook(url=settings.WEBHOOK_URL)

'''
###########################
# Sample message processing
###########################
@bot.message_handler(commands=['test'])
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

'''


##################
# Helper functions
##################
def get_user(message):
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
    return user


def get_location(message):
    location = None
    if message.location != None:
        location = Location.objects.create(latitude=message.location.latitude, longitude=message.location.longitude)
    return location


def get_photo(message):
    file_id = message.photo[-1].file_id
    image_info = bot.get_file(file_id)
    image_data = bot.download_file(image_info.file_path)
    return Photo.objects.create(upload=io.BytesIO(image_data))


##################
# Message handlers
##################
@bot.message_handler(commands=['start'])
def show_start_help(message):
    bot.send_message(chat_id=message.chat.id, text=constants.BOT_START_MESSAGE)


@bot.message_handler(commands=['help'])
def show_help(message):
    bot.send_message(chat_id=message.chat.id, text=constants.BOT_HELP_MESSAGE)


@bot.message_handler(commands=['add'])
def add_location(message):
    bot.send_message(chat_id=message.chat.id, text=constants.ON_ADD_COMMAND_MESSAGE)


def get_last_location(user):
    last_location = None
    try:
        last_location = Location.objects.get(user=user, is_editable=True)
    except Exception as err:
        print("get last location error: ", err)
    return last_location


@bot.message_handler(func=lambda message: message.text not in constants.BOT_KNOWN_COMMANDS, content_types=['location','text','photo'])
def put_data(message):
    try:
        user = get_user(message)
        location = get_last_location(user)
        location_was_none = location is None
        if location_was_none:
            location = Location.objects.create(user=user)

        if message.location:
            # save old location as non editable
            if location_was_none is False:
                location.is_editable = False
                location.save()
                location = Location.objects.create(user=user)
            # save new location data
            location.latitude = message.location.latitude
            location.lonigude = message.location.longitude
            location.save()
            answer = constants.ON_LOCATION_SAVED_MESSAGE

        elif message.text:
            location.text = message.text
            location.save()
            answer = constants.ON_TEXT_SAVED_MESSAGE

        else:
            photo = get_photo(message)
            photo.location = location
            photo.save()
            answer = constants.ON_PHOTO_SAVED_MESSAGE

        bot.send_message(chat_id=message.chat.id, text=answer)

    except Exception as err:
        print("error put data: ", err)


@bot.message_handler(commands=['list'])
def list_locations(message):
    try:
        user = get_user(message)
        answer = constants.ON_LIST_LOCATIONS_MESSAGE
        if user.locations:
            answer += "\n"
            for loc in user.locations:
                loc_str = str(loc) + "\n"
                answer += loc_str
        else:
            answer += constants.IS_NULL_MESSAGE
        bot.send_message(chat_id=message.chat.id, text=answer)
    except Exception as err:
        print("error list locations: ", err)


@bot.message_handler(commands=['reset'])
def reset_locations(message):
    try:
        user = get_user(message)
        for loc in user.locations:
            loc.delete()
        bot.send_message(chat_id=message.chat.id, text=constants.ON_RESET_COMMAND_MESSAGE)
    except Exception as err:
        print("error reset locations: ", err)


@csrf_exempt
@require_POST
def pull_messages(request):
    print("pull_messages")
    print(request.body.decode("utf-8"))
    updates = Update.de_json(request.body.decode("utf-8"))
    bot.process_new_updates([updates])
    return HttpResponse(status=200)



###############
# Test db views
###############
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
