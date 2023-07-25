######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : settings
# @created     : Tuesday Aug 17, 2021 16:51:00 CST
#
# @description :
######################################################################

import os


def get_managed():
    return True  # os.getenv("environment", None) == "TEST"
