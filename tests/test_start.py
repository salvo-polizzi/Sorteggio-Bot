import pytest
from pytest_mock import MockerFixture
from src.bot import start, Update, User
from telegram import Message, Chat
from datetime import datetime

def test_start(mocker: MockerFixture) -> None:
    # arrange
    mock_user = User(id=0, first_name='user', is_bot=True, username='user')
    mock_update = Update(0, message=Message(0, new_chat_members=mock_user, chat=Chat(0, type='GROUP'), date=datetime.now()))
    mock_message = Message
    mocker.patch.object(mock_message, 'reply_text', return_value=None)
    spy = mocker.spy(mock_message, 'reply_text')

    # act
    start(mock_update, None)

    # assert
    assert spy.call_count == 1
    assert spy.spy_return == None