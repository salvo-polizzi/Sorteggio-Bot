from ast import Call
from calendar import c
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
sorteggio_users_command = "sorteggioManuale"
sorteggio_all_users_command = "sorteggioUtenti"
sorteggio_non_admin_command = "sorteggioNonAdmin"

str1 = "Il numero di partecipanti al sorteggio è minore del\
	numero di partecipanti da sorteggiare"
str2 = "Il comando deve essere utilizzato specificando il numero\
	di partecipanti da sorteggiare"


help_str = f"Comandi disponibili:\
	\n\n /{sorteggio_admin_command} N - Per sorteggiare N utenti amministratori\
	\n /{sorteggio_users_command} N username1 username2 (specificare la @) ecc... - Per sorteggiare N utenti scelti (che hanno scritto\
	almento una volta nel gruppo da quando il bot è stato inserito)\
	\n /{sorteggio_all_users_command} N - Per sorteggiare N utenti qualsiasi (che hanno scritto\
	almento una volta nel gruppo da quando il bot è stato inserito)\
	\n /{sorteggio_non_admin_command} N - Per sorteggiare N utenti non amministratori\
	(che hanno scritto almento una volta nel gruppo da quando il bot è stato inserito)"


#defining first methods
def start(update: Update, context: CallbackContext):
	update.message.reply_text(
		"Ciao :), scrivi /help per vedere i comandi disponibili.")	

def help(update: Update, context: CallbackContext):
	update.message.reply_text(help_str)

def unknown(update: Update, context: CallbackContext):
	update_chat_data(update, context)
	update.message.reply_text(
		" '%s' non è un comando valido" % update.message.text)

def get_admin_list_obj(update: Update, context: CallbackContext) ->list[ChatMember]:

	chat_id = context._chat_id_and_data[0]

	admin_list_obj = b.get_chat_administrators(chat_id)

	return admin_list_obj		

def get_list_str(user_list_obj: list[ChatMember]) ->list[str]:

	lista = []
	for u in user_list_obj:
		username = u.user.username

		if username != None:
			lista.append(" @" + username + " " + u.user.full_name)
		else:
			lista.append(u.user.full_name) 

	return lista

def get_sorteggiati_list_obj(update: Update, user_list_obj, obj_n: int, estrazioni_n: int) ->list[ChatMember]:

	sorteggiati_list = [] 

	if estrazioni_n > obj_n:
		update.message.reply_text(str1)
		return None	

	for x in range(0, estrazioni_n):

		index = random.randint(0, obj_n-1) #estrazione sorteggio

		sorteggiati_list.append(user_list_obj.pop(index))		
		obj_n = obj_n - 1	

	return sorteggiati_list	



def get_chosen_users(context: CallbackContext) -> list[ChatMember]:
	
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

	

#def get_username_list(context: CallbackContext):
	list_members = get_all_members_list_obj(context)

	list_username = []
	for member in list_members:
		list_username.append(member.user.username)

	return list_username


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
		update.message.reply_text(str2)
		return		
	
	if command.find(sorteggio_admin_command) != -1:
		list_obj = get_admin_list_obj(update, context)
	elif command.find(sorteggio_all_users_command) != -1:
		list_obj = get_all_members_list_obj(context)
	elif command.find(sorteggio_non_admin_command) != -1:
		list_obj = get_non_administrators(update, context)
	
	list_str = get_list_str(list_obj)

	update.message.reply_text("Lista di partecipanti al Sorteggio:" + '\n\n' + str(list_str))	

	sorteggiati_list_obj = get_sorteggiati_list_obj(update, 
		list_obj, len(list_obj), estrazioni_n)

	if sorteggiati_list_obj == None:
		return

	sorteggiati_list_str = get_list_str(sorteggiati_list_obj)	
	update.message.reply_text("Risulato:" + '\n\n' + str(sorteggiati_list_str) )
	

def sorteggio_utenti_scelti(update: Update, context: CallbackContext):

	lista_utenti = get_chosen_users(context)

	if lista_utenti == None:
		update.message.reply_text("Inserisci uno o più username validi")
		return
	
	estrazioni_n = 0

	try:
		estrazioni_n = int(context.args[0])
	except(IndexError, ValueError):
		update.message.reply_text(str2)
		return	

	lista_utenti_str = get_list_str(lista_utenti)

	update.message.reply_text("Lista di partecipanti al Sorteggio:" + '\n\n' + str(lista_utenti_str))		

	if estrazioni_n > len(lista_utenti):
		update.message.reply_text(str1)
		return None		
	
	lista_utenti_sorteggiati = []

	for x in range(0, estrazioni_n):
		index = random.randint(0, len(lista_utenti) - 1)
		lista_utenti_sorteggiati.append(lista_utenti.pop(index))

	update.message.reply_text("Lista di utenti sorteggiati: \n" + str(get_list_str(lista_utenti_sorteggiati)))
	
def update_chat_data(update: Update, context: CallbackContext) ->None:
	#ATTENZIONE: affinche funzioni per bene, cioè possa leggere tutti i messaggi
	#group privacy mode deve essere off

	chat_members_dict = context.chat_data
	chat_members_list_obj = list(chat_members_dict.values())

	for chat_member in chat_members_list_obj:
		if chat_member.user.id == update.effective_message.from_user.id:
			return

	chat_id = context._chat_id_and_data[0]
	chat_member = b.get_chat_member(chat_id, update.effective_message.from_user.id)
	chat_members_dict[len(chat_members_dict)] = chat_member

	#print(context.chat_data)

def get_all_members_list_obj(context: CallbackContext) ->list[ChatMember]:

	chat_members_list_obj = list(context.chat_data.values())
	return chat_members_list_obj

def get_non_administrators(update: Update, context: CallbackContext) -> list[ChatMember]:

	list_members = get_all_members_list_obj(context)

	list_non_admin = []
	for member in list_members:
		if member.status != "administrator" and member.status != "creator":
			list_non_admin.append(member)

	return list_non_admin

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler(sorteggio_admin_command, sorteggio))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler(sorteggio_users_command, sorteggio_utenti_scelti))
updater.dispatcher.add_handler(CommandHandler(sorteggio_all_users_command, sorteggio))
updater.dispatcher.add_handler(CommandHandler(sorteggio_non_admin_command, sorteggio))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) 
# Filters out not command messages
updater.dispatcher.add_handler(MessageHandler(Filters.text, update_chat_data))

updater.start_polling()		