# import json
# import sys
import time
# from flask import render_template
from rq import get_current_job
from app import create_app
from app.database import db
# from app.user.models import User
from app.task.models import Task
# from app.email import send_email

app = create_app()  # pylint: disable=invalid-name
app.app_context().push()


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
            task.user.add_message(contents=f'Task {task.name} (id: {task.id} ) has completed')
            task.user.add_notification('unread_message_count', task.user.new_messages())
        db.session.commit()


def example(seconds):
    _set_task_progress(0)
    for i in range(1, seconds + 1):
        _set_task_progress(100 * i // seconds)
        time.sleep(1)


# def export_posts(user_id):
#     try:
#         user = User.query.get(user_id)
#         _set_task_progress(0)
#         data = []
#         i = 0
#         total_posts = user.posts.count()
#         for post in user.posts.order_by(Post.timestamp.asc()):
#             data.append({'body': post.body,
#                          'timestamp': post.timestamp.isoformat() + 'Z'})
#             i += 1
#             _set_task_progress(i // total_posts * 100)
#
#         send_email('[My Flask App] Your blog posts',
#                    sender=app.config['ADMINS'][0], recipients=[user.email],
#                    text_body=render_template('email/export_posts.txt', user=user),
#                    html_body=render_template('email/export_posts.html', user=user),
#                    attachments=[('posts.json', 'application/json',
#                                  json.dumps({'posts': data}, indent=4))],
#                    sync=True)
#     except:
#         _set_task_progress(100)
#         app.logger.error('Unhandled exception', exc_info=sys.exc_info())
