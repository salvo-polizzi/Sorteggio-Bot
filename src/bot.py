import random

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from telegram import *

#taking the token
first_line = open("token.txt").readline()
token = first_line
	
updater = Updater(token, use_context=True)

b = Bot(token)

sorteggio_admin_command = "sorteggioAdmin"

#defining first methods
def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Ciao :), scrivi /help per vedere i comandi disponibili.")	

def nulla(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Hahahhaha che comando inutile")

def help(update: Update, context: CallbackContext):
	update.message.reply_text("Comandi disponibili:" +
	'\n' + "/sorteggioAdmin - Per sorteggiare gli amministratori"+
	'\n'+ "/nulla - Comando inutile")

def unknown(update: Update, context: CallbackContext):
	update.message.reply_text(
		" '%s' non è un comando valido" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Sorry I can't recognize you , you said '%s'" % update.message.text)