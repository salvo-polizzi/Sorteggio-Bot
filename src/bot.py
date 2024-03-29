
import random

from telegram.ext.updater import Updater
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from telegram import *

try:
	from src.vars import *
except:
	from vars import *

from typing import *

#taking the token
try:
	first_line = open("src/token.txt").readline()
except:
	first_line = open("Sorteggio-Bot/src/token.txt").readline()

token = first_line
	
updater = Updater(token, use_context=True)

b = Bot(token)

#defining first methods
def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Ciao :), scrivi /help per vedere i comandi disponibili.")	

def help(update: Update, context: CallbackContext):
	update.message.reply_text(HELP)

def unknown(update: Update, context: CallbackContext):
	update_chat_data(update, context)
	update.message.reply_text(
		" '%s' non è un comando valido" % update.message.text)

def get_admin_list(context: CallbackContext) -> List[ChatMember]:

	chat_id = context._chat_id_and_data[0]

	admin_list_obj = b.get_chat_administrators(chat_id)

	return admin_list_obj		

def user_list_to_string(user_list_obj: List[ChatMember]) -> List[str]:

	lista = []
	for u in user_list_obj:
		username = u.user.username

		if username != None:
			lista.append(" @" + username + " " + u.user.full_name)
		else:
			lista.append(u.user.full_name) 

	return lista

def get_sorteggiati_list(update: Update, user_list_obj: List[ChatMember], estrazioni_n: int) -> List[ChatMember]:

	sorteggiati_list = [] 

	if estrazioni_n > len(user_list_obj):
		update.message.reply_text(RISPOSTE["numero_partecipanti"])
		return None	

	for x in range(0, estrazioni_n):

		index = random.randint(0, len(user_list_obj)-1) #estrazione sorteggio

		sorteggiati_list.append(user_list_obj.pop(index))			

	return sorteggiati_list	



def get_chosen_users(context: CallbackContext) -> List[ChatMember]:
	
	user_list = []

	for x in range(1, len(context.args)):
		user_list.append((context.args[x])[1:])
	
	all_member_list = get_all_members_list_obj(context)
	chosen_user_list = []
	for user in user_list:
		found = False
		for member in all_member_list:
			if user == member.user.username:
				chosen_user_list.append(member)
				found = True
		if not found:
			return None
	return chosen_user_list


def sorteggio(update: Update, context: CallbackContext):

	chat_id = context._chat_id_and_data[0]
	chat_type =  b.get_chat(chat_id).type

	if chat_type != "group" and  chat_type != "supergroup":
		update.message.reply_text("Non è possibile eseguire il comando in questo ambiente")
		return
	
	command = update.message.text_html

	try:
		estrazioni_n = int(context.args[0])
	except(IndexError, ValueError):
		update.message.reply_text(RISPOSTE["specificare_partecipanti"])
		return		
	
	if command.find(COMANDI["sorteggio_admin"]) != -1:
		list_obj = get_admin_list(context)
	elif command.find(COMANDI["sorteggio_tutti_utenti"]) != -1:
		list_obj = get_all_members_list_obj(context)
	elif command.find(COMANDI["sorteggio_non_admin"]) != -1:
		list_obj = get_non_administrators(context)
	elif command.find(COMANDI["sorteggio_utenti_scelti"]) != -1:
		list_obj = get_chosen_users(context)
		if list_obj == None:
			update.message.reply_text("Inserisci uno o più username validi")
			return
	
	list_str = user_list_to_string(list_obj)

	update.message.reply_text("Lista di partecipanti al Sorteggio:" + '\n\n' + str(list_str))	

	sorteggiati_list_obj = get_sorteggiati_list(update, 
		list_obj, estrazioni_n)

	if sorteggiati_list_obj == None:
		return

	sorteggiati_list_str = user_list_to_string(sorteggiati_list_obj)	
	update.message.reply_text("Risultato:" + '\n\n' + str(sorteggiati_list_str) )
	

def update_chat_data(update: Update, context: CallbackContext) -> None:
	#ATTENZIONE: affinche funzioni per bene, cioè possa leggere tutti i messaggi
	#group privacy mode deve essere off (da prima ancora di avere aggiunto il bot al gruppo)

	chat_members_dict = context.chat_data
	chat_members_list_obj = list(chat_members_dict.values())

	for chat_member in chat_members_list_obj:
		if chat_member.user.id == update.effective_message.from_user.id:
			return

	chat_id = context._chat_id_and_data[0]
	chat_member = b.get_chat_member(chat_id, update.effective_message.from_user.id)
	chat_members_dict[len(chat_members_dict)] = chat_member

	#print(context.chat_data)

def get_all_members_list_obj(context: CallbackContext) -> List[ChatMember]:

	chat_members_list_obj = list(context.chat_data.values())
	return chat_members_list_obj

def get_non_administrators(context: CallbackContext) -> List[ChatMember]:

	list_members = get_all_members_list_obj(context)

	list_non_admin = []
	for member in list_members:
		if member.status != "administrator" and member.status != "creator":
			list_non_admin.append(member)

	return list_non_admin

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler(COMANDI["sorteggio_admin"], sorteggio))
updater.dispatcher.add_handler(CommandHandler(COMANDI["sorteggio_utenti_scelti"], sorteggio))
updater.dispatcher.add_handler(CommandHandler(COMANDI["sorteggio_tutti_utenti"], sorteggio))
updater.dispatcher.add_handler(CommandHandler(COMANDI["sorteggio_non_admin"], sorteggio))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) 
# Filters out not command messages
updater.dispatcher.add_handler(MessageHandler(Filters.text, update_chat_data))

updater.start_polling()		