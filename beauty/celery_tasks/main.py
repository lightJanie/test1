from celery import Celery
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'beauty.settings'

celery_app=Celery('beauty')
# 导入celery配置
celery_app.config_from_object('beauty.settings')
# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.user_tasks'])
