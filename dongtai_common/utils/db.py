import copy

from django.db import models
from django.db.models import Expression


class SearchLanguageMode(Expression):
    template = "MATCH( %(expressions)s ) AGAINST ( %(search_keyword)s IN NATURAL LANGUAGE MODE )"

    def __init__(self, expressions, search_keyword):
        super().__init__(output_field=models.IntegerField())
        self.search_keyword = search_keyword
        for expression in expressions:
            if not hasattr(expression, "resolve_expression"):
                raise TypeError("%r is not an Expression" % expression)
        self.expressions = expressions

    def resolve_expression(
        self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False
    ):
        c = self.copy()
        c.is_summary = summarize
        for pos, expression in enumerate(self.expressions):
            c.expressions[pos] = expression.resolve_expression(
                query, allow_joins, reuse, summarize, for_save
            )
        return c

    def as_sql(self, compiler, connection, template=None):
        sql_expressions, sql_params = [], []
        for expression in self.expressions:
            sql, params = compiler.compile(expression)
            sql_expressions.append(sql)
            sql_params.extend(params)
        template = template or self.template
        data = {
            "expressions": ",".join(sql_expressions),
            "search_keyword": "%s",
        }
        sql_params.append(self.search_keyword)
        return template % data, sql_params

    def get_source_expressions(self):
        return self.expressions

    def set_source_expressions(self, expressions):
        self.expressions = expressions
