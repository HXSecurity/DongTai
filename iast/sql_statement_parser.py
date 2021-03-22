#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 10:43
# software: PyCharm
# project: webapi

"""
sql语句解析器，用于越权检测中，对sql语句的拆分和比对
"""
import sqlparse
from sqlparse.sql import Where


class SqlParser:
    def __init__(self, statement):
        self._original_sql_statement = statement
        self._sql_parsed = None
        self._tokens = None
        self._wheres = None
        self.parse()

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        self._tokens = tokens

    def get_token_size(self):
        return [len(_) for _ in self.tokens]

    @property
    def sql_parsed(self):
        return self._sql_parsed

    @sql_parsed.setter
    def sql_parsed(self, sql_parsed):
        self._sql_parsed = sql_parsed

    @property
    def original_sql_statement(self):
        return self._original_sql_statement

    @original_sql_statement.setter
    def original_sql_statement(self, statement):
        self._original_sql_statement = statement

    @property
    def wheres(self):
        return self._wheres

    @wheres.setter
    def wheres(self, wheres):
        self._wheres = wheres

    @staticmethod
    def __parse_query_condition(tokens):
        return list(filter(lambda x: isinstance(x, Where), tokens))

    def parse(self):
        self.sql_parsed = sqlparse.parse(self.original_sql_statement)
        self.tokens = [_.tokens for _ in self.sql_parsed]
        self.wheres = [self.__parse_query_condition(_) for _ in self.tokens]

    def __eq__(self, o: object) -> bool:
        """
        重写eq方法，用于重写sql语句相等的判断规则
        - 表名相同
        - 查询参数相同
        - 查询条件相同
        :param o:
        :return:
        """
        func = lambda x, y: x == y
        if len(self.wheres) == len(o.wheres):
            return all([func(x, y) for x, y in zip(self.wheres, o.wheres)])
        return False


if __name__ == '__main__':
    sql = 'select * from article where id=1 and user_id=1 order by id limit 0,1'
    parser = SqlParser(sql)
    print(parser.tokens)
    print(parser.get_token_size())
    print(parser.wheres)

    new_sql = 'select * from article where id=1 and user_id=1 and name=\'owef\' order by id limit 0,1'
    new_sql = 'select * from article where id=1 and user_id=1 order by id limit 0,1'
    new_parser = SqlParser(sql)
    print(new_parser.wheres)
    print(parser == new_parser)

    new_parser.sql_parsed[0].sql.Comparison(parser.tokens[0])
