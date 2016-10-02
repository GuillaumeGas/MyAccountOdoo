# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Transaction (models.Model):
    _name = 'account.transaction'

    name = fields.Char(string="Nom", required=True)
    value = fields.Float(string="Valeur", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today())
    validated = fields.Boolean(string="Validated", default=True)

    account_id = fields.Many2one('account.account', string="Compte", required=True)

    @api.model
    def create(self, values):
        if (self.validated):
            self.account_id.value -= self.value

    @api.onchange('date')
    def _change_date(self):
        transaction_date = fields.Date.from_string(self.date)
        current_date = fields.Date.from_string(fields.Date.today())
        diff_date = current_date - transaction_date
        if diff_date.months >= 0 or (diff_date.months == 0 and diff_date.days >= 0):
            self.validated = True
        else:
            self.validated = False
