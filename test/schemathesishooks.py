import time

import schemathesis


@schemathesis.hooks.register
def add_case(context, case, response):
    time.sleep(0.1)
