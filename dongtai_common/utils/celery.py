import celery

class DongTaiConvertPoolTask(celery.Task):

    def apply_async(self,
                    args=None,
                    kwargs=None,
                    task_id=None,
                    producer=None,
                    link=None,
                    link_error=None,
                    shadow=None,
                    **options):

        super().apply_async(self,
                            args=args,
                            kwargs=kwargs,
                            task_id=task_id,
                            producer=producer,
                            link=link,
                            link_error=link_error,
                            shadow=shadow,
                            **options)

@app.task(base=DongTaiConvertPoolTask)
def add(x, y):
    raise KeyError()
