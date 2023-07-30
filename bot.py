#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""

import os
import logging
from dotenv import load_dotenv
from sheets import get_list, get_event_details_links, get_ccas_by_category, get_random_cca, get_ccas_by_zone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Top Level Callback Data
EVENT, PROGS, CCAINFO, ZONING, PERF, START_OVER, END = range(7)
# States of conversation
FIRST, MENU, CCA_MENU, FETCHING_DATA_BY_CATEGORY, ZONING_MENU, RANDOM, FETCHING_DATA_BY_ZONE, CCA_INFO_BY_CATEGORY, CCA_INFO_BY_ZONE = range(9)


def start(update: Update, context: CallbackContext) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    if not context.user_data.get(START_OVER):
        user = update.message.from_user
        logger.info("User %s started the conversation.", user.first_name)
    
    #Starting layer: Event details, Programme schedule (link to website), CCA information 
    text = "Click on 'Event Details' to learn more about SLF and our history, 'Programmes Schedule' to discover our lineup of exciting activities in store, and 'CCA Information' to discover everything about our student groups. "
    
    keyboard = [
        [
            InlineKeyboardButton(text="Event Details", callback_data=str(EVENT)),
            InlineKeyboardButton(text="Programmes Schedule", callback_data=str(PROGS)),
        ],

        [
            InlineKeyboardButton(text="Performance Schedule", callback_data=str(PERF)),
            InlineKeyboardButton(text="CCA Information", callback_data=str(CCAINFO)),

        ],

        [
            InlineKeyboardButton(text="Zoning", callback_data=str(ZONING)),
            InlineKeyboardButton(text="Done", callback_data=str(END)),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
        
    else:
       update.message.reply_text(
            "Welcome to NUS Student Life Fair 2022! This is our specially created Telegram bot that " 
            "will help you navigate all the Student Groups you can imagine. \n\nHope you enjoy the event!")
       
       update.message.reply_text(text=text, reply_markup=reply_markup)
    
    context.user_data[START_OVER] = False
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST

def event(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    # gets links from sheet "Event Details"
    links = get_event_details_links()
    # maps to buttons, appends back button
    keyboard = list(map(lambda link : [InlineKeyboardButton(link[0], url=link[1]), ], links))
    keyboard.append([InlineKeyboardButton("Back", callback_data=str(START_OVER)), ])
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Visit our website here!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
    #     ],
    #     [
    #         InlineKeyboardButton("Check out our instagram!", url='https://www.instagram.com/nusstudentlife/?hl=en'),
    #     ],
    #     [
    #         InlineKeyboardButton("Join our telegram channel!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
    #     ],
    #     [
    #         InlineKeyboardButton("Get the SLF 22' map!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
    #     ],
    #     [
    #         InlineKeyboardButton("Back", callback_data=str(START_OVER)),
    #     ]
    # ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Insert write-up about SLF here :-) ", reply_markup=reply_markup
    )
    
    context.user_data[START_OVER] = True
    
    return MENU

def progs(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Schedule here!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
        ],
        [
            InlineKeyboardButton("Back", callback_data=str(START_OVER)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Click the link below to access our programmes schedule for our event!", reply_markup=reply_markup
    )
    
    context.user_data[START_OVER] = True
    
    return MENU

#--------------- Newly added Performance Schedule Section -----------------#
# to change performance schedule link 

def perf(update: Update, context: CallbackContext) -> int:

    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Schedule here!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
        ],
        [
            InlineKeyboardButton("Back", callback_data=str(START_OVER)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Click the link below to access our performance schedule for our event!", reply_markup=reply_markup
    )
    
    context.user_data[START_OVER] = True
    
    return MENU


def ccainfo(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("NUSSU", callback_data='NUSSU'),
            InlineKeyboardButton("Performing Arts", callback_data='ARTS'),
            InlineKeyboardButton("Sports Groups", callback_data='SPORTS'),
        ],
        [
            InlineKeyboardButton("Interest Groups", callback_data='IG'),
            InlineKeyboardButton("Registered Societies", callback_data='REGSOC')
        ],
        [
            InlineKeyboardButton("RANDOM!", callback_data= str(RANDOM)),
            InlineKeyboardButton("Back", callback_data=str(START_OVER))
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="There are 5 broad categories of CCAs in NUS. Take your pick! If you don't know how to choose, "
        "click 'Random' below for a surprise!", reply_markup=reply_markup)
    
    context.user_data[START_OVER] = True
    
    return CCA_MENU

def zoning(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    query.answer()
    
    keyboard = [
      [
        InlineKeyboardButton("SLF Map!", url='https://nus.edu.sg/osa/orientation/events/student-life-fair'),
      ],
      [
        InlineKeyboardButton("Zone 1", callback_data='Zone 1'),
      ],
      [
        InlineKeyboardButton("Zone 2", callback_data='Zone 2'),
      ],
      [
        InlineKeyboardButton("UTown", callback_data='UTown'),
      ],
      [
        InlineKeyboardButton("Back", callback_data=str(START_OVER)),
      ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="There are 3 zones in SLF this year! Where do you want to explore?", reply_markup=reply_markup)
    
    context.user_data[START_OVER] = True
    
    return ZONING_MENU

def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')

    return END

def fetch_buttons_by_categories(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    category = query.data
    
    query.answer()

    ccas = get_ccas_by_category(category)
    
    keyboard1 = [[InlineKeyboardButton(
        cca[1], callback_data=str(cca[1])) ] for cca in ccas]
    
    keyboard2 = [[InlineKeyboardButton("Back", callback_data=str(START_OVER))]]
    
    keyboard = keyboard1 + keyboard2
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="Take a pick!", reply_markup=reply_markup)
    
    return FETCHING_DATA_BY_CATEGORY

def fetch_buttons_by_zones(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    zone = query.data
    
    query.answer()

    ccas = get_ccas_by_zone(zone)
    
    keyboard1 = [[InlineKeyboardButton(
        cca[1], callback_data=str(cca[1])) ] for cca in ccas]
    
    keyboard2 = [[InlineKeyboardButton("Back", callback_data=str(START_OVER))]]
    
    keyboard = keyboard1 + keyboard2
    reply_markup = InlineKeyboardMarkup(keyboard)
        
    message = "These are the booths in " + str(zone) + "!"
        
    query.edit_message_text(
        text=message, reply_markup=reply_markup)
    
    return FETCHING_DATA_BY_ZONE

def fetch_info_by_category(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    querydata = query.data
    context.user_data["key"] = querydata
    
    query.answer()
    
    #checking for the category chosen
    intended = context.user_data["key"]  
    
    working_list = get_list()
    
    for items in working_list:
        if items[1] == intended:
            text = str(
                'Name: ' + str(items[1]) + '\n\n'
                'Description: ' + str(items[3]) + '\n\n'
                'NUSync: ' + str(items[4]) + '\n\n'
                'Website: ' + str(items[5]) + '\n\n'
                'Instagram: ' + str(items[6]) + '\n\n'
                'Location: ' + str(items[7]) + '\n\n'
                )
            
            context.user_data["data"] = items
            
            keyboard = [[InlineKeyboardButton("Back", callback_data=str(START_OVER))]]

            reply_markup = InlineKeyboardMarkup(keyboard)
    
            query.edit_message_text(text=text, reply_markup=reply_markup)
        
            pass
    
    return CCA_INFO_BY_CATEGORY

def fetch_info_by_zone(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    querydata = query.data
    context.user_data["key"] = querydata
    
    query.answer()
    
    #checking for the category chosen
    intended = context.user_data["key"]  
    
    working_list = get_list()
    
    for items in working_list:
        if items[1] == intended:
            text = str(
                'Name: ' + str(items[1]) + '\n\n'
                'Description: ' + str(items[3]) + '\n\n'
                'NUSync: ' + str(items[4]) + '\n\n'
                'Website: ' + str(items[5]) + '\n\n'
                'Instagram: ' + str(items[6]) + '\n\n'
                'Location: ' + str(items[7]) + '\n\n'
                )
            
            context.user_data["data"] = items
            
            keyboard = [[InlineKeyboardButton("Back", callback_data=str(START_OVER))]]

            reply_markup = InlineKeyboardMarkup(keyboard)
    
            query.edit_message_text(text=text, reply_markup=reply_markup)
        
            pass
    
    return CCA_INFO_BY_ZONE

def random_cca(update: Update, context: CallbackContext) -> int:
    """Show new choice of buttons"""
    query = update.callback_query   
    query.answer()
    
    items = get_random_cca()
    
    text = str(
        'Name: ' + str(items[1]) + '\n\n'
        'Description: ' + str(items[3]) + '\n\n'
        'NUSync: ' + str(items[4]) + '\n\n'
        'Website: ' + str(items[5]) + '\n\n'
        'Instagram: ' + str(items[6]) + '\n\n'
        'Location: ' + str(items[7]) + '\n\n'
        )
    
    keyboard = [
        [InlineKeyboardButton("Want another random CCA?", callback_data=str(RANDOM))],
        [InlineKeyboardButton("Back", callback_data=str(START_OVER))],
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(text=text, reply_markup=reply_markup)
        
    return CCA_MENU

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ["BOT_TOKEN"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(event, pattern='^' + str(EVENT) + '$'),
                CallbackQueryHandler(perf, pattern='^' + str(PERF) + '$'),
                CallbackQueryHandler(progs, pattern='^' + str(PROGS) + '$'),
                CallbackQueryHandler(ccainfo, pattern='^' + str(CCAINFO) + '$'),
                CallbackQueryHandler(zoning, pattern='^' + str(ZONING) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(END) + '$'),
            ],
            
            MENU: [
                CallbackQueryHandler(start, pattern='^' + str(START_OVER) + '$'),
            ],
            
            CCA_MENU: [
                CallbackQueryHandler(start, pattern='^' + str(START_OVER) + '$'),
                CallbackQueryHandler(random_cca, pattern='^' + str(RANDOM) + '$'),
                CallbackQueryHandler(fetch_buttons_by_categories)
            ],
            
            FETCHING_DATA_BY_CATEGORY: [
                CallbackQueryHandler(ccainfo, pattern='^' + str(START_OVER) + '$'),
                CallbackQueryHandler(fetch_info_by_category)
            ],
            
            ZONING_MENU: [
                CallbackQueryHandler(start, pattern='^' + str(START_OVER) + '$'),
                CallbackQueryHandler(fetch_buttons_by_zones)
            ],

            FETCHING_DATA_BY_ZONE: [
                CallbackQueryHandler(zoning, pattern='^' + str(START_OVER) + '$'),
                CallbackQueryHandler(fetch_info_by_zone)
            ],
            
            CCA_INFO_BY_CATEGORY: [
                CallbackQueryHandler(ccainfo, pattern='^' + str(START_OVER) + '$'),
            ],
            
            CCA_INFO_BY_ZONE: [
                CallbackQueryHandler(zoning, pattern='^' + str(START_OVER) + '$'),
            ],
            
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()