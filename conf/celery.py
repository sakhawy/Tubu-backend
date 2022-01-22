from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from django.conf import settings
from celery.utils.log import get_task_logger
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
django.setup()

app = Celery('conf')

logger = get_task_logger(__name__)

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	logger.info(f"STARTING SCHEDULED TASKS")
	sender.add_periodic_task(
		10,
		check_online_videos_task.s(), 
		name='periodic vid check'
	)

@app.task(name="check_online_videos_task")
def check_online_videos_task():
	logger.info(f"Check")
	download_video_task.s().apply_async()
	return

@app.task(name="download_video_task")
def download_video_task():
	import time
	logger.info(f"Downloading")
	time.sleep(20)
	logger.info(f"Done")
	return