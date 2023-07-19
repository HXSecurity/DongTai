#!/usr/bin/env python
# datetime: 2021/7/16 下午12:17
from dongtai_common.utils import const


class Replay:
    """
    封装重放操作为单独的类
    """

    def __init__(self, replay):
        self.replay = replay
        self.vul = None

    @staticmethod
    def do_replay(replay):
        replay_handler = Replay(replay)
        status = replay_handler.has_relation_id()
        if status is False:
            pass

    def has_relation_id(self):
        return self.replay.relation_id is None

    @staticmethod
    def replay_failed(replay, timestamp):
        """
        当重放请求处理失败时,执行该方法
        """
        replay.update_time = timestamp
        replay.verify_time = timestamp
        replay.state = const.SOLVED
        replay.result = const.RECHECK_ERROR
        replay.save(update_fields=["update_time", "verify_time", "state", "result"])
