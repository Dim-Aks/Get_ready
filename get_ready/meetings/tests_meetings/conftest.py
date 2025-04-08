from datetime import datetime

import pytest
from django.contrib.auth.models import User
from ..models import Comment, Meeting

date_meet = datetime(2026, 4, 8, 15, 51, 39, 670011)


# тестовый пользователь
@pytest.fixture
def user():
    return User.objects.create(
        username='testuser',
        password='password')


# тестовый пользователь 2
@pytest.fixture
def another_user():
    return User.objects.create_user(
        username='anotheruser',
        password='testpass123'
    )


# тестовая встреча
@pytest.fixture
def meeting(user):
    return Meeting.objects.create(author=user,
                                     reason_to_meet='Test Meeting',
                                     meeting_place='Test meeting_place',
                                     address='Test Meeting address',
                                     what_to_do='Test Meeting what_to_do',
                                     dress_code='Test Meeting dress_code',
                                     date_meeting=date_meet,
                                     )


# тестовый комментарий к встрече
@pytest.fixture
def comment(user, meeting):
    return Comment.objects.create(
        meeting=meeting,
        author=user,
        text='This is a test comment'
    )