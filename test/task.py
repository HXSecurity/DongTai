import unittest

from core.tasks import heartbeat, search_vul_from_method_pool
from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):

    def test_celery_beat(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.HOURS, )

        import json
        heartbeat_task = PeriodicTask.objects.filter(name='engine.heartbeat').first()
        if heartbeat_task:
            heartbeat_task.task = 'core.tasks.heartbeat'
            heartbeat_task.interval = schedule
            heartbeat_task.save(update_fields=['task', 'interval'])
        else:
            PeriodicTask.objects.create(
                interval=schedule,
                name='engine.heartbeat',
                task='core.tasks.heartbeat',
                args=json.dumps([]),
            )

        schedule, created = IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.MINUTES, )
        update_agent_task = PeriodicTask.objects.filter(name='engine.update_agent_status').first()
        if update_agent_task:
            update_agent_task.task = 'core.tasks.update_agent_status'
            update_agent_task.interval = schedule
            update_agent_task.save()
        else:
            PeriodicTask.objects.create(
                interval=schedule,
                name='engine.update_agent_status',
                task='core.tasks.update_agent_status',
                args=json.dumps([]),
            )

        schedule, created = IntervalSchedule.objects.get_or_create(every=1, period=IntervalSchedule.DAYS, )
        update_sca_task = PeriodicTask.objects.filter(name='engine.update_sca').first()
        if update_sca_task:
            update_sca_task.task = 'core.tasks.update_sca'
            update_sca_task.interval = schedule
            update_sca_task.save()
        else:
            PeriodicTask.objects.create(
                interval=schedule,
                name='engine.update_sca',
                task='core.tasks.update_sca',
                args=json.dumps([]),
            )

    def test_agent_status_update(self):
        from core.tasks import update_agent_status
        update_agent_status()

    def test_heart_beat(self):
        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lingzhi_engine.settings")
        os.environ.setdefault("debug", "true")
        import django
        django.setup()
        heartbeat()


if __name__ == '__main__':
    unittest.main()
