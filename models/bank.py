# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Bank (models.Model):
    _name = 'account.bank'

    name = fields.Char(string="Name", required=True)
    value = fields.Float(string="Value", compute='_get_value')
    account_ids = fields.One2many('account.account', 'bank_id', string="Accounts")

    @api.multi
    def _get_value(self):
        for r in self:
            value = 0.0
            for account in r.account_ids:
                value += account.value
            r.value = value
