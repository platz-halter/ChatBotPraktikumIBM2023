#Import Modules#--------------------------
import telebot
from telebot import types
import json, requests
import de,us

#Settings#--------------------------------
TOKEN = '################'
LANGUAGE = us

preset1 = 'p1'
preset2 = 'p2'
preset3 = 'p3'


offenses_api = 'https://161.156.45.202:12443/api/siem/offenses'
types_api = 'https://161.156.45.202:12443/api/siem/offense_types'

#Startup#---------------------------------
client = telebot.TeleBot(TOKEN)
requests.packages.urllib3.disable_warnings() 

@client.message_handler(commands=['start'])
def on_start(message):
    chat_id = message.chat.id
    message_id = message.id
    
    client.delete_message(chat_id, message_id)
    client.send_message(chat_id, "Hello!")
    print('BOT started succesfully')

#Custom Modules#--------------------------
def get_type(type_num):
    response = requests.get(types_api, headers={'SEC':'######-###-#####-####-######', 'Range': 'items=0-80'}, verify=False)
    json = response.json()
    objects_amount = len(json)

    for i in range(0, objects_amount):
        selected_type = json[i]["id"]
        if selected_type == type_num:
            offense_type = json[i]["name"]
            return(offense_type)

def module_search(search):
    try:
        print(search.text)
        client.delete_message(search.chat.id, search.id), client.delete_message(search_message.chat.id, search_message.id)  
        client.send_message(search.chat.id, f"Searching for: {search.text}")
    except:
        print(search)

def module_offenses(filter, bmsg):
    print('Offenses')
    response = requests.get(offenses_api, headers={'SEC':'####-###-#####-#####-ea#####b', 'Range':'items=0-100'}, verify=False)
    print(response.request.__dict__)
    json = response.json()
    objects_amount = len(json)

    client.send_message(bmsg.chat.id, "Here you go:")

    if filter == 'last5': objects_amount = 5
    elif "last5" in filter: objects_amount = 5
    elif "last10" in filter: objects_amount = 10
    
    
    for i in range(0, objects_amount):
        id = json[i]['id']
        description = json[i]['description']
        status = json[i]['status']
        magnitude = json[i]['magnitude']
        offense_source = json[i]['offense_source']
        offense_type_id = json[i]['offense_type']
        offense_type = get_type(offense_type_id)
        relevance = json[i]['relevance']

        default_message = f"ID: {id} \nOffense source: {offense_source} \nType: {offense_type}\n"

        #Default Fiter 
        if filter == 'all': 
            message = default_message + f"\n\n{description}"
            client.send_message(bmsg.chat.id, message)
            continue
        if filter == 'last5':
            message = default_message + f"\n\n{description}"
            client.send_message(bmsg.chat.id, message)
            continue
        #Advanced Filter 
        message = default_message

        if "mag4" in filter and magnitude >= 4:
            message = message + f"Magnitude: {magnitude}"
        elif "mag4" in filter and magnitude < 4:
            continue
        
        if "relevance1" in filter and relevance >= 1:
            message = message + f"\nRelevance: {relevance}"
        elif "relevance1" in filter and relevance <= 0:
            continue

        if "active" in filter and status == "OPEN":
            message = message + f"\nStatus: {status}"
        elif "active" in filter and status == "CLOSED":
            continue

        if "last5" in filter or "last10" in filter:
            message = message + f"\n\n{description}"

        client.send_message(bmsg.chat.id, message)

    client.delete_message(bmsg.chat.id, bmsg.id)
    return
        
#User Interface#--------------------------
@client.message_handler(commands=['help', 'commands', '?', 'h', 'menu', 'interface', 'H'])
def main_interface(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    offenses = types.InlineKeyboardButton('Offenses', callback_data = "main_offenses")
    search = types.InlineKeyboardButton(LANGUAGE.search, callback_data="main_search")
    nothing = types.InlineKeyboardButton(LANGUAGE.do_nothing, callback_data="nothing")
    markup.add(offenses,search,nothing)

    global bot_message
    bot_message = bot_message = client.send_message(message.chat.id, LANGUAGE.service_message, reply_markup=markup)
    client.delete_message(message.chat.id, message.id) #DEL user command

def search_interface(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    preset1 = types.InlineKeyboardButton("Preset1", callback_data="search_preset1")
    preset2 = types.InlineKeyboardButton("Preset2", callback_data="search_preset2") 
    preset3 = types.InlineKeyboardButton("Preset3", callback_data="search_preset3")
    search  = types.InlineKeyboardButton(LANGUAGE.search , callback_data="search_custom")
    nothing = types.InlineKeyboardButton(LANGUAGE.do_nothing , callback_data="nothing")
    markup.add(preset1,preset2,preset3,search, nothing)
    
    client.delete_message(message.chat.id, message.id)

    global bot_message
    bot_message = client.send_message(message.chat.id, LANGUAGE.option, reply_markup=markup)

def offenses_interface(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    show_all = types.InlineKeyboardButton(LANGUAGE.all, callback_data="offenses_all")
    magnitude3 = types.InlineKeyboardButton("Magnitude>3", callback_data="offenses_mag4")
    last5 = types.InlineKeyboardButton(LANGUAGE.last5, callback_data="offenses_last5")
    active = types.InlineKeyboardButton(LANGUAGE.active, callback_data="offenses_active")
    more_filters = types.InlineKeyboardButton("More filters" , callback_data="offenses_filters")
    nothing = types.InlineKeyboardButton(LANGUAGE.do_nothing , callback_data="nothing")
    markup.add(show_all, last5, more_filters,nothing)

    client.delete_message(message.chat.id, message.id)

    global bot_message
    bot_message = client.send_message(message.chat.id, LANGUAGE.option, reply_markup=markup)

def offenses_filters(message):
    global active_filters
    active_filters = []

    markup = types.InlineKeyboardMarkup(row_width=1)
    mag4 = types.InlineKeyboardButton("Mag4", callback_data="offenses_filters_mag4")
    active = types.InlineKeyboardButton("Active", callback_data="offenses_filters_active")
    nothing = types.InlineKeyboardButton(LANGUAGE.do_nothing , callback_data="nothing")
    confirm = types.InlineKeyboardButton("Confirm", callback_data="offenses_filters_confirm")
    last5 = types.InlineKeyboardButton("Last5", callback_data="offenses_filters_last5")
    last10 = types.InlineKeyboardButton("Last10", callback_data="offenses_filters_last10")
    markup.add(mag4, active, last5,last10,confirm, nothing)

    client.delete_message(message.chat.id, message.id)

    global bot_message
    bot_message = client.send_message(message.chat.id, LANGUAGE.option, reply_markup=markup)
#Interface responses----------------------
@client.callback_query_handler(func=lambda call:True)
def interface_navigation(callback):
    if callback.data == "nothing":
        client.delete_message(bot_message.chat.id, bot_message.id)
        return
    #Main interface
    if callback.data == 'main_search': search_interface(bot_message)
    if callback.data == 'main_offenses': offenses_interface(bot_message)    
    #Search interface
    if callback.data == 'search_preset1': module_search(preset1)
    if callback.data == 'search_preset2': module_search(preset2)
    if callback.data == 'search_preset3': module_search(preset3)
    if callback.data == 'search_custom' :
        global search_message
        search_message = client.send_message(bot_message.chat.id, LANGUAGE.search_message)
        client.register_next_step_handler(search_message, module_search)
    #Offenses interface
    if callback.data == 'offenses_all': module_offenses('all', bot_message)
    if callback.data == 'offenses_last5': module_offenses('last5', bot_message)
    if callback.data == 'offenses_active': module_offenses('active', bot_message)
    if callback.data == 'offenses_filters': offenses_filters(bot_message)
    #Offenses Filters interface
    if callback.data == 'offenses_filters_mag4':
        active_filters.insert(0, "mag4")
    if callback.data == 'offenses_filters_active': active_filters.insert(0, "active")
    if callback.data == 'offenses_filters_last5': active_filters.insert(0, "last5")
    if callback.data == 'offenses_filters_last10': active_filters.insert(0, "last10")
    if callback.data == 'offenses_filters_confirm': module_offenses(active_filters, bot_message)

client.infinity_polling()

