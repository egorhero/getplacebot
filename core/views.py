import telebot
from telebot.types import Update
from getplacebot import settings
from core.models import User, Location, Photo
from core import constants
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core import files
from io import BytesIO


##########
# Init bot
##########
bot = telebot.TeleBot(settings.TELEBOT_API_TOKEN)
bot.set_webhook(url=settings.WEBHOOK_URL)


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
            user = User.objects.create(id=u.id, is_bot=u.is_bot, first_name=u.first_name, username=u.username, last_name=u.last_name, language_code=u.language_code)
        except Exception as err:
            print("object creation error: ", err)
    return user


def get_last_location(user, create):
    last_location = None
    try:
        last_location = Location.objects.get(user=user, is_editable=True)
    except Exception as err:
        print("get last location error: ", err)
        if create:
            last_location = Location.objects.create(user=user)
    return last_location


def get_photo(message):
    file_id = message.photo[-1].file_id
    image_info = bot.get_file(file_id)
    image_data = bot.download_file(image_info.file_path)
    fp = BytesIO()
    fp.write(image_data)
    photo = Photo(link=str(image_info.file_path))
    photo.upload.save(str(file_id)+".jpg", files.File(fp))
    photo.save()
    return photo


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


@bot.message_handler(func=lambda message: message.text not in constants.BOT_KNOWN_COMMANDS, content_types=['location','text','photo'])
def put_data(message):
    try:
        user = get_user(message)

        if message.location:
            location = get_last_location(user, False)
            if location:
                location.is_editable = False
                location.save()
            location = Location.objects.create(user=user)
            location.latitude = message.location.latitude
            location.longitude = message.location.longitude
            location.save()
            answer = constants.ON_LOCATION_SAVED_MESSAGE

        elif message.text:
            location = get_last_location(user, True)
            location.text += message.text
            location.save()
            answer = constants.ON_TEXT_SAVED_MESSAGE

        else:
            location = get_last_location(user, True)
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
        cid = message.chat.id
        bot.send_message(chat_id=cid, text=constants.ON_LIST_LOCATIONS_MESSAGE)
        if user.locations:
            for loc in user.locations:
                bot.send_location(chat_id=cid, latitude=loc.latitude, longitude=loc.longitude)
                for photo in loc.photos:
                    bot.send_photo(chat_id=cid, photo=photo.upload.file)
                bot.send_message(chat_id=cid, text=loc.text)
        else:
            bot.send_message(chat_id=cid, text=constants.IS_NULL_MESSAGE)
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
    print(request.body.decode("utf-8"))
    updates = Update.de_json(request.body.decode("utf-8"))
    bot.process_new_updates([updates])
    return HttpResponse(status=200)


#def acme_challenge(request):
#    return HttpResponse(settings.ACME_CHALLENGE_CONTENT)
