# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Transaction (models.Model):
    _name = 'account.transaction'

    name = fields.Char(string="Name", required=True)
    value = fields.Float(string="Value", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today())
    validated = fields.Boolean(string="Validated", default=True)

    account_id = fields.Many2one('account.account', string="Account",
                                 required=True, ondelete='cascade')
    category_id = fields.Many2one('account.category', string="Category",
                                  required=True, ondelete='set null')

    @api.model
    def create(self, values):
        if (values['validated']):
            account = self.env['account.account'].search([('id', '=', values['account_id'])])
            account.value += values['value']
        return super(Transaction, self).create(values)

    @api.multi
    def write(self, values):
        if ('validated' in values):
            if (values['validated']):
                account = self.env['account.account'].search([('id', '=', self.account_id.id)])
                value = self.value
                if ('value' in values):
                    value = values['value']
                account.value += value
        return super(Transaction, self).write(values)

    @api.onchange('date')
    def _change_date(self):
        transaction_date = fields.Date.from_string(self.date)
        current_date = fields.Date.from_string(fields.Date.today())
        diff_date = current_date - transaction_date
        if diff_date.days >= 0:
            self.validated = True
        else:
            self.validated = False
