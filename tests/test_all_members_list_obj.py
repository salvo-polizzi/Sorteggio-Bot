import pytest
from pytest_mock import MockerFixture
from src.bot import get_all_members_list_obj
from telegram import ChatMember, Bot
from telegram.ext import CallbackContext, Dispatcher, ContextTypes
import queue

def test_all_members_list_obj(mocker: MockerFixture) -> None:
    #arrange
    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    chat_id = 1111
    mock_context = CallbackContext(disp)

    mocker.patch.object(CallbackContext, "chat_data", return_value = None)
    spy_chat_data = mocker.spy(CallbackContext, "chat_data")


    #act
    res = get_all_members_list_obj(mock_context)

    #assert
    for member in res:
        assert type(member) == ChatMember
    assert spy_chat_data.spy_return == None