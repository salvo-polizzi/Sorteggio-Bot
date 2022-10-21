import pytest
from pytest_mock import MockerFixture
from src.bot import get_chosen_users, User
from telegram import ChatMember, Bot
from telegram.ext import Dispatcher, CallbackContext
import queue

import src.bot

def test_get_chosen_users(mocker: MockerFixture) -> None:

    #arrange
    username_1 = "user1"
    username_2 = "user2"

    mock_user_1 = User(id=0, is_bot=True, first_name="a", username = username_1)
    mock_user_2 = User(id=1, is_bot=True, first_name="b", username = username_2)

    mock_chat_members = []
    mock_chat_members.append( ChatMember(mock_user_1, "administrator") )
    mock_chat_members.append( ChatMember(mock_user_2, "administrator") )

    mocker.patch.object(src.bot, "get_all_members_list_obj", return_value=mock_chat_members)
    
    q = queue.Queue()
    disp = Dispatcher(Bot, q)

    args_1 = [None, "@" + username_1, "@" + username_2]
    args_2 = [None, "@" + username_1, "@" + username_2, "@lol"]

    mock_context_1 = CallbackContext(disp)
    mock_context_1.args = args_1

    mock_context_2 = CallbackContext(disp)
    mock_context_2.args = args_2

    #act
    res_1 = get_chosen_users(mock_context_1)
    res_2 = get_chosen_users(mock_context_2)

    #assert
    assert len(res_1) == len(args_1)-1

    for element in res_1:
        assert type(element) == ChatMember

    assert res_2 is None    

    

      