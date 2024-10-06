import maya
from flask import url_for


class TestNotifications:

    def test_get_notifications(self, testapp, authenticated_user):
        authenticated_user.add_notification(name='panda', data='bear')
        authenticated_user.save()

        response = testapp.get(url_for('user.notifications'))

        notification = response.json[0]
        assert notification['name'] == 'panda'
        assert notification['data'] == 'bear'

    def test_get_notifications_since_yesterday(self, testapp, authenticated_user):
        authenticated_user.add_notification(name='panda', data='bear')
        authenticated_user.save()

        yesterday = maya.when('yesterday').datetime().date()
        response = testapp.get(url_for('user.notifications') + f'?since={yesterday}')

        assert len(response.json) == 1

    def test_get_notifications_since_tomorrow(self, testapp, authenticated_user):
        authenticated_user.add_notification(name='panda', data='bear')
        authenticated_user.save()

        tomorrow = maya.when('tomorrow').datetime().date()
        response = testapp.get(url_for('user.notifications') + f'?since={tomorrow}')

        assert len(response.json) == 0
