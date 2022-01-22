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

# Local imports after django setup 
from utils import utils


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
		settings.PERIODIC_CHECK_INTERVAL,
		check_online_videos_task.s(), 
		name='periodic vid check'
	)

@app.task(name="check_online_videos_task")
def check_online_videos_task():
	from api import models

	# Check if we have any videos with the state "ONLINE"
	online_qs = utils.get_online_videos_queue()
	downloading_qs = utils.get_downloading_videos_queue()

	remaining_threads = settings.MAX_THREADS - len(downloading_qs)

	if remaining_threads > 0:
		for _ in range(remaining_threads):
			if online_qs:
				logger.info(f"{len(online_qs)} videos: 'ONLINE'. {len(downloading_qs)} videos: 'DOWNLOADING'. (MAX_THREADS: {settings.MAX_THREADS}).")
				download_video_task.s(
					online_qs.pop(0)
				).apply_async()

	else:
		logger.info(f"{len(online_qs)} videos: 'ONLINE'. {len(downloading_qs)} videos: 'DOWNLOADING'. NOTHING TO BE DONE FOR NOW.")
	
	return

@app.task(name="download_video_task")
def download_video_task(video):
	logger.info(f"Downloading")
	utils.download_video(video["id"])

	downloading_qs = utils.get_downloading_videos_queue()
	logger.info(f"{len(downloading_qs)} videos: 'DOWNLOADING'. (MAX_THREADS: {settings.MAX_THREADS}).")
	
	return