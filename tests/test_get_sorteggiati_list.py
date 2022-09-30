import pytest
from pytest_mock import MockerFixture
from src.bot import get_sorteggiati_list, Update, User
from telegram import Message, Chat, ChatMember
from datetime import datetime
import random

#test della funzione nel caso in cui il numero di estrazioni è maggiore del numero di partecipanti
def test_get_sorteggiati_list_1(mocker: MockerFixture) -> None:
    #arrange
    mock_user = User(id=0, first_name='user', is_bot=True, username='user')
    mock_update = Update(0, message=Message(0, new_chat_members=mock_user, chat=Chat(0, type='GROUP'), date=datetime.now()))
    mock_message = Message
    
    mock_n_estrazioni = 2
    mock_user_list_obj = []
    mock_user_list_obj.append(ChatMember(mock_user, "administrator"))

    mocker.patch.object(mock_message, "reply_text", return_value=None)
    spy = mocker.spy(mock_message, "reply_text")

    #act
    res = get_sorteggiati_list(mock_update, mock_user_list_obj, mock_n_estrazioni)

    #assert
    assert res is None
    assert spy.call_count == 1
    assert spy.spy_return == None

#test della funzione nel caso in cui il numero di estrazioni è minore del numero di partecipanti
def test_get_sorteggiati_list_2(mocker: MockerFixture) -> None:
    #arrange
    mock_user = User(id=0, first_name='user', is_bot=True, username='user')
    mock_update = Update(0, message=Message(0, new_chat_members=mock_user, chat=Chat(0, type='GROUP'), date=datetime.now()))
    mock_random = random
    
    mock_n_estrazioni = 1
    mock_user_list_obj = []
    mock_user_list_obj.append(ChatMember(mock_user, "administrator"))

    mocker.patch.object(mock_random, "randint", return_value=0)
    spy = mocker.spy(mock_random, "randint")

    #act
    res = get_sorteggiati_list(mock_update, mock_user_list_obj, mock_n_estrazioni)

    #assert
    for user in res:
        assert type(user) == ChatMember

    assert spy.call_count == 1
    assert spy.spy_return == 0