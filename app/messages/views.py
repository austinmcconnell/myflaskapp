from flask import Blueprint, render_template, request, url_for
from flask_login import current_user, login_required
import maya

from app.messages.models import Message

message_bp = Blueprint(name='messages',  # pylint: disable=invalid-name
                       import_name=__name__, template_folder='templates')


@message_bp.route('/messages')
@login_required
def messages():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    current_user.update(last_message_read_time=maya.now().datetime())
    current_user.add_notification('unread_message_count', 0)

    messages = current_user.messages.order_by(Message.timestamp.desc())\
                                    .paginate(page=page, per_page=per_page, error_out=False)

    next_url = url_for('messages.messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('messages.messages', page=messages.prev_num) if messages.has_prev else None

    return render_template('messages.html',
                           messages=messages.items,
                           next_url=next_url,
                           prev_url=prev_url)
