from typing import List
import pytest
from pytest_mock import MockerFixture
from src.bot import user_list_to_string, User
from telegram import ChatMember
from datetime import datetime

def test_user_list_to_string(mocker: MockerFixture) -> None:
    #arrange
    mock_user_1 = User(id=0, is_bot=True, first_name="user", username = "user")
    mock_user_2 = User(id=1, is_bot=True, first_name="nouser")

    mock_user_list_obj = []
    mock_user_list_obj.append(ChatMember(mock_user_1, "administrator"))
    mock_user_list_obj.append(ChatMember(mock_user_2, "administrator"))

    #act
    res = user_list_to_string(mock_user_list_obj)

    #assert
    for element in res:
        assert type(element) == str