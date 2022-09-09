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

def get_admin_list_obj(update: Update, context: CallbackContext):

	chat_id = context._chat_id_and_data[0]
	chat_type =  b.get_chat(chat_id).type

	if chat_type != "group" and  chat_type != "supergroup":
		update.message.reply_text("Non è possibile eseguire il comando in questo ambiente")
		return None

	admin_list_obj = b.get_chat_administrators(chat_id)

	return admin_list_obj		

def get_list_str(user_list_obj):

	lista = []
	for u in user_list_obj:
		username = u.user.username

		if username != None:
			lista.append(" @" + username + " " + u.user.full_name)
		else:
			lista.append(u.user.full_name) 

	return lista

def get_sorteggiati_list_obj(update: Update, user_list_obj, obj_n: int, estrazioni_n: int):

	sorteggiati_list = [] 

	if estrazioni_n > obj_n:
		update.message.reply_text("Il numero di partecipanti al sorteggio è minore del" +
			" numero di partecipanti da sorteggiare")
		return None	

	for x in range(0, estrazioni_n):

		index = random.randint(0, obj_n-1) #estrazione sorteggio

		sorteggiati_list.append(user_list_obj.pop(index))		
		obj_n = obj_n - 1	

	return sorteggiati_list	


def sorteggio(update: Update, context: CallbackContext):

	try:
		estrazioni_n = int(context.args[0])
	except(IndexError):
		update.message.reply_text("Il comando deve essere utilizzato specificando il numero"+
			" di utenti da sorteggiare")
		return		

	command = update.message.text_html
	end = command.find(" ")
	command = command[1: end]
	#print(command)

	if command == sorteggio_admin_command:
		list_obj = get_admin_list_obj(update, context)	
	else:
		print("Qualcosa è andato storto")

	if list_obj == None:
		return

	list_str = get_list_str(list_obj)

	update.message.reply_text("Lista di partecipanti al Sorteggio:" + '\n\n' + str(list_str))	

	sorteggiati_list_obj = get_sorteggiati_list_obj(update, 
		list_obj, len(list_obj), estrazioni_n)

	if sorteggiati_list_obj == None:
		return

	sorteggiati_list_str = get_list_str(sorteggiati_list_obj)	
	update.message.reply_text("Risulato:" + '\n\n' + str(sorteggiati_list_str) )


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('nulla', nulla))
updater.dispatcher.add_handler(CommandHandler(sorteggio_admin_command, sorteggio))
updater.dispatcher.add_handler(CommandHandler('help', help))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) 
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()		