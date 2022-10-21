import pytest
from pytest_mock import MockerFixture
from src.bot import get_non_administrators, User
from telegram import ChatMember, Bot
from telegram.ext import Dispatcher, CallbackContext
import queue

import src.bot

def test_get_non_administrators(mocker: MockerFixture) -> None:

    #arrange
    username_1 = "user1"
    username_2 = "user2"
    username_3 = "user3"

    mock_user_1 = User(id=0, is_bot=True, first_name="a", username = username_1)
    mock_user_2 = User(id=1, is_bot=True, first_name="b", username = username_2)
    mock_user_3 = User(id=2, is_bot=True, first_name="c", username = username_3)

    mock_chat_members = []
    mock_chat_members.append( ChatMember(mock_user_1, "administrator") )
    mock_chat_members.append( ChatMember(mock_user_2, "member") )
    mock_chat_members.append( ChatMember(mock_user_3, "creator") )

    mocker.patch.object(src.bot, "get_all_members_list_obj", return_value=mock_chat_members)

    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    mock_context = CallbackContext(disp)

    #act
    res = get_non_administrators(mock_context)

    #assert
    for element in res:
        assert type(element) is ChatMember
        assert element.status != "administrator" and element.status != "creator"

    

    

      