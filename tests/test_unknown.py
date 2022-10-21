import pytest
from pytest_mock import MockerFixture
from src.bot import unknown, Update, User
from telegram import Message, Chat, Bot
from telegram.ext import CallbackContext, Dispatcher
from datetime import datetime
import queue
import src.bot

def test_unknown(mocker: MockerFixture) -> None:
    #arrange
    mock_user = User(id=0, first_name='user', is_bot=True, username='user')
    mock_update = Update(0, message=Message(0, new_chat_members=mock_user, chat=Chat(0, type='GROUP'), date=datetime.now()))

    q = queue.Queue()
    disp = Dispatcher(Bot, q)
    chat_id = 1111
    mock_context = CallbackContext(disp)

    mock_message = Message

    mocker.patch("src.bot.update_chat_data", return_value = None)
    mocker.patch.object(mock_message, "reply_text", return_value = None)

    spy_chat_data = mocker.spy(src.bot, "update_chat_data")
    spy_reply_text = mocker.spy(mock_message, "reply_text")


    #act
    unknown(mock_update, mock_context)

    #assert
    assert spy_chat_data.call_count == 1
    assert spy_reply_text.call_count == 1

    assert spy_chat_data.spy_return == None
    assert spy_reply_text.spy_return == None
