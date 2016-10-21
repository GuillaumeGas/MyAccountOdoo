# -*- coding: utf-8 -*-
from openerp import models, fields


class BankStatement(models.Model):
    _name = 'account.bank_statement'

    _sql_constraint = [('name_unique', 'UNIQUE(name)', 'The name must be unique')]

    name = fields.Char(string="Name", default=fields.Date.today())
    account_statement_ids = fields.One2many(
        'account.account_statement', 'bank_statement_id', string="Account statements")

    def _get_default_name(self):
        date = fields.Date.today()
        for r in self:
            return str(date.month) + str(date.year)
