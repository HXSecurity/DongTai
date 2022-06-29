from celery import shared_task
from django.apps import apps
from django.db import transaction
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.signals import RealTimeSignalProcessor


from celery.apps.worker import logger

@shared_task
def handle_save(pk, app_label, model_name):
    logger.info(f'handle_save to es: {model_name} pk: {pk}')
    sender = apps.get_model(app_label, model_name)
    instance = sender.objects.get(pk=pk)
    registry.update(instance)
    registry.update_related(instance)


class DTCelerySignalProcessor(RealTimeSignalProcessor):

    def handle_save(self, sender, instance, **kwargs):
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        if instance.__class__ in registry._models:
            logger.info(f'handle_save to es: {model_name} ')
            transaction.on_commit(
                lambda: handle_save.delay(instance.pk, app_label, model_name))
