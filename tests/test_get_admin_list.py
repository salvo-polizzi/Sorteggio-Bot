import pytest
from pytest_mock import MockerFixture
from src.bot import get_admin_list, User
from telegram import Chat, Bot, ChatMember
from telegram.ext import CallbackContext, Dispatcher
from datetime import datetime
import queue

def test_get_admin_list(mocker: MockerFixture) -> None:

    #arrange
    mock_user = User(id=0, is_bot=True, first_name="user", username = "user")
    mock_chat_members = ChatMember(mock_user, "administrator")
    
    mocker.patch.object(Bot, "get_chat_administrators", return_value=mock_chat_members)
    spy = mocker.spy(Bot, "get_chat_administrators")

    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    chat_id = 1111

    mock_context = CallbackContext(disp)
    mock_context._chat_id_and_data = (chat_id, None)
    

    #act
    get_admin_list(mock_context)

    #assert
    assert spy.call_count == 1
    assert spy.spy_return == mock_chat_members