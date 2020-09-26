

BOT_KNOWN_COMANDS = {
    0: "/start",
    1: "/add",
    2: "/list",
    3: "/reset",
}

BOT_INPUT_STATES = {
    0: "command",
    1: "coords",
    2: "address",
    3: "pictures",
}

BOT_HELP_MESSAGE = \
'''
Just type some of this commands \n
and input your data!
\n
/add location (address and photo) \n
\n
/list locations (you noted)
\n
/reset locations (old data)
\n
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

ON_ADD_COMMAND_MESSAGE = "Put some location (text, photo) data to save it."
ON_LOCATION_SAVED_MESSAGE = "Location saved."
ON_TEXT_SAVED_MESSAGE = "Text saved."
ON_PHOTO_SAVED_MESSAGE = "Photo saved."
ON_LIST_LOCATIONS_MESSAGE = "List of noted locations..."
ON_RESET_COMMAND_MESSAGE = "All location data was dropped."
IS_NULL_MESSAGE = "is null"
