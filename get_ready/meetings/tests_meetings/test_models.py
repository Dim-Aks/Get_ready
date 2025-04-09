import pytest

from .conftest import date_meet
from ..models import Comment, Meeting


# тест модели встреч
@pytest.mark.django_db
def test_meeting_creation(user, meeting):
    assert Meeting.objects.count() == 1
    assert meeting.author == user
    assert meeting.reason_to_meet =='Test Meeting'
    assert meeting.meeting_place == 'Test meeting_place'
    assert meeting.address == 'Test Meeting address'
    assert meeting.what_to_do == 'Test Meeting what_to_do'
    assert meeting.dress_code == 'Test Meeting dress_code'
    assert meeting.date_meeting == date_meet


# тест модели комментариев
@pytest.mark.django_db
def test_comment_creation(user, meeting, comment):
    assert Comment.objects.count() == 1
    assert comment.meeting == meeting
    assert comment.author == user
    assert comment.text == 'This is a test comment'
    assert str(comment) == 'This is a test comment'