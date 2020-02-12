from flask import url_for


class TestNotifications:

    def test_set_last_read_time(self, testapp, authenticated_user):
        assert authenticated_user.last_message_read_time is None

        testapp.get(url_for('messages.messages'))

        assert authenticated_user.last_message_read_time is not None
