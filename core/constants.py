BOT_KNOWN_COMMANDS = ["/start", "/add", "/list", "/reset"]

BOT_HELP_MESSAGE = \
'''
Just type some of this commands \n
and input your data! \n
/add location (address and photo) \n
/list locations (you noted) \n
/reset locations (old data) \n
'''

BOT_START_MESSAGE = \
'''
Hello, I'm a getplacebot! \n
I can help you to save, get and notify \n
about locations which you liked or noted! \n
%s \n
Thank you for using my service! \n
Have a nice day!
''' % (BOT_HELP_MESSAGE)

ON_ADD_COMMAND_MESSAGE = "Waiting for location (text, photo) data..."
ON_LOCATION_SAVED_MESSAGE = "Location saved. Ok!"
ON_TEXT_SAVED_MESSAGE = "Text saved. Ok!"
ON_PHOTO_SAVED_MESSAGE = "Photo saved. Ok!"
ON_LIST_LOCATIONS_MESSAGE = "List of noted locations..."
ON_RESET_COMMAND_MESSAGE = "All location data was dropped."
IS_EMPTY_MESSAGE = "is empty"
