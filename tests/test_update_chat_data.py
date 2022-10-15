import pytest
from pytest_mock import MockerFixture
from src.bot import update_chat_data, User
from telegram import ChatMember, Bot, Update, Message, Chat
from telegram.ext import Dispatcher, CallbackContext
from datetime import datetime
import queue

import src.bot

def test_update_chat_data_1(mocker: MockerFixture) -> None:

    #arrange
    username_1 = "user1"
    user_1 = User(id=0, is_bot=True, first_name="a", username = username_1)

    chat_member_1 = ChatMember(user_1, "administrator")
    my_dict = {0: chat_member_1}

    chat_id = 1111
    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    mock_context = CallbackContext(disp)
    mock_context._chat_id_and_data = [chat_id, my_dict]

    username_2 = "user2"
    user_2 = User(id=1, is_bot=True, first_name="b", username = username_2)
    chat_member_2 = ChatMember(user_2, "administrator")

    mock_update = Update(0, message=Message(0, from_user=user_2, chat=Chat(chat_id, type='GROUP'), date=datetime.now()))     

    mocker.patch.object(Bot, "get_chat_member", return_value = chat_member_2)
    spy_get_chat_member = mocker.spy(Bot, "get_chat_member")

    #act
    update_chat_data(mock_update, mock_context)

    #assert  
    assert my_dict == {0: chat_member_1, 1: chat_member_2}
    assert spy_get_chat_member.call_count == 1
    assert spy_get_chat_member.spy_return == chat_member_2

def test_update_chat_data_2(mocker: MockerFixture) -> None:

    #arrange
    username_1 = "user1"
    user_1 = User(id=0, is_bot=True, first_name="a", username = username_1)

    chat_member_1 = ChatMember(user_1, "administrator")
    my_dict = {0: chat_member_1}

    chat_id = 1111
    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    mock_context = CallbackContext(disp)
    mock_context._chat_id_and_data = [chat_id, my_dict]

    mock_update = Update(0, message=Message(0, from_user=user_1, chat=Chat(chat_id, type='GROUP'), date=datetime.now()))     

    spy_get_chat_member = mocker.spy(Bot, "get_chat_member")

    #act
    update_chat_data(mock_update, mock_context)

    #assert  
    assert my_dict == {0: chat_member_1}
    assert spy_get_chat_member.call_count == 0





       

    

      