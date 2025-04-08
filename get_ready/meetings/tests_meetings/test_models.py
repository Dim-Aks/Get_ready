from datetime import datetime

import pytest
from django.contrib.auth.models import User
from ..models import Comment, Meeting

date_meet = datetime.now()

@pytest.fixture
def user():
    user = User.objects.create(username='testuser', password='password')
    return user

@pytest.fixture
def meeting(user):
    meeting = Meeting.objects.create(author=user,
                                     reason_to_meet='Test Meeting',
                                     meeting_place='Test Meeting',
                                     address='Test Meeting',
                                     what_to_do='Test Meeting',
                                     dress_code='Test Meeting',
                                     date_meeting=date_meet,
                                     )
    return meeting

@pytest.mark.django_db
def test_meeting_creation(user, meeting):

    assert Meeting.objects.count() == 1
    assert meeting.author == user
    assert meeting.reason_to_meet =='Test Meeting'
    assert meeting.meeting_place == 'Test Meeting'
    assert meeting.address == 'Test Meeting'
    assert meeting.what_to_do == 'Test Meeting'
    assert meeting.dress_code == 'Test Meeting'
    assert meeting.date_meeting == date_meet


@pytest.mark.django_db
def test_comment_creation(user, meeting):
    comment = Comment.objects.create(meeting=meeting, author=user, text='This is a test comment')

    assert Comment.objects.count() == 1
    assert comment.meeting == meeting
    assert comment.author == user
    assert comment.text == 'This is a test comment'
    assert str(comment) == 'This is a test comment'