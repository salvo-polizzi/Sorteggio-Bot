from ast import Call
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
sorteggio_words_command = "sorteggioParole"
sorteggio_all_users_command = "sorteggioUtenti"
sorteggio_non_admin_command = "sorteggioNonAdmin"

str1 = "Il numero di partecipanti al sorteggio è minore del\
	numero di partecipanti da sorteggiare"
str2 = "Il comando deve essere utilizzato specificando il numero\
	di utenti da sorteggiare"
str3 = "Il comando deve essere utilizzato specificando il numero\
	di parole da sorteggiare"
str4 = "Il numero di parole al sorteggio è minore del\
	numero di parole da sorteggiare"

help_str = "Comandi disponibili:\
	\n\n /sorteggioAdmin N - Per sorteggiare N utenti amministratori\
	\n /sorteggioParole N parola1 parola2 ecc... - Per sortegggiare N parole\
	\n /sorteggioUtenti N - Per sorteggiare N utenti qualsiasi (che hanno scritto\
	almento una volta nel gruppo da quando il bot è stato inserito)"


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

def get_list_str(user_list_obj) ->list[str]:

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



def get_words_list(context: CallbackContext) ->list[str]:

	words_list = []

	for x in range(1, len(context.args)):
		words_list.append(context.args[x])
	return words_list


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
		if command.find(sorteggio_admin_command) != -1 or command.find(sorteggio_all_users_command) != -1:
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
	

def sorteggio_parole(update: Update, context: CallbackContext):

	lista_parole = get_words_list(context)

	estrazioni_n = 0

	try:
		estrazioni_n = int(context.args[0])
	except(IndexError, ValueError):
		update.message.reply_text(str3)
		return	

	update.message.reply_text("Lista di parole: \n" + str(lista_parole))		

	if estrazioni_n > len(lista_parole):
		update.message.reply_text(str4)
		return None		
	
	lista_parole_sorteggiate = []

	for x in range(0, estrazioni_n):
		index = random.randint(0, len(lista_parole) - 1)
		lista_parole_sorteggiate.append(lista_parole.pop(index))

	update.message.reply_text("Lista di parole sorteggiate: \n" + str(lista_parole_sorteggiate))

def update_chat_data(update: Update, context: CallbackContext):
	#ATTENZIONE: affinche funzioni per bene, cioè possa leggere tutti i messaggi
	#group privacy mode deve essere off

	messages_dict = context.chat_data
	messages_dict[len(messages_dict)] = update.effective_message

	#print(context.chat_data)

def get_all_members_list_obj(context: CallbackContext) ->list[ChatMember]:

	chat_id = context._chat_id_and_data[0]

	messages_list_obj = list(context.chat_data.values())
	#print(messages_list_obj)

	members_list_obj = []

	for message in messages_list_obj:

		chat_member = b.get_chat_member(chat_id, message.from_user.id)
		duplicato = True

		try:
			index = members_list_obj.index(chat_member)
		except(ValueError):
			duplicato = False

		if not duplicato:
			members_list_obj.append(chat_member)
				
		#print(chat_member)

	#print(members_list_obj)
	
	return members_list_obj

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
updater.dispatcher.add_handler(CommandHandler(sorteggio_words_command, sorteggio_parole))
updater.dispatcher.add_handler(CommandHandler(sorteggio_all_users_command, sorteggio))
updater.dispatcher.add_handler(CommandHandler(sorteggio_non_admin_command, sorteggio))

# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown)) 
# Filters out not command messages
updater.dispatcher.add_handler(MessageHandler(Filters.text, update_chat_data))

updater.start_polling()		