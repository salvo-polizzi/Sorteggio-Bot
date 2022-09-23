import pytest
from pytest_mock import MockerFixture
from src.bot import help, Update, User
from telegram import Message, Chat
from datetime import datetime

def test_help(mocker: MockerFixture) -> None:
    #arrange
    mock_user = User(id=0, is_bot=True, first_name="user", username = "user")
    mock_update = Update(0, message=Message(message_id=0, date=datetime.now(), new_chat_members = mock_user, chat =Chat(0, type = "GROUP")))
    mock_message = Message
    mocker.patch.object(mock_message, "reply_text", return_value=None)
    spy = mocker.spy(mock_message, "reply_text")

    #act
    help(mock_update, None)

    #assert
    assert spy.call_count == 1
    assert spy.spy_return == None

    