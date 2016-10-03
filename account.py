# -*- coding: utf-8 -*-
from openerp import models, fields
from datetime import timedelta


class Account (models.Model):
    _name = 'account.account'

    name = fields.Char(string="Name", required=True)
    value = fields.Float(string="Value", default=0.0)
    start_date = fields.Date(compute='_get_start_date')
    end_date = fields.Date(compute='_get_end_date')

    transaction_ids = fields.One2many(
        'account.transaction', 'account_id', string="Transactions")

    def _get_start_date(self):
        for r in self:
            r.start_date = fields.Date.today()

    def _get_end_date(self):
        for r in self:
            s_date = fields.Date.from_string(r.start_date)
            duration = timedelta(days=31)
            r.end_date = s_date + duration
