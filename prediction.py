# -*- coding: utf-8 -*-
from openerp import models, fields


class Prediction (models.Model):
    _name = 'account.prediction'
    _inherits = {'account.transaction': 'transaction_id'}

    predict_value = fields.Float(string="Value", compute='_get_value')
    start_date = fields.Date(string="Start date", default=fields.Date.today())

    transaction_id = fields.Many2one('account.transaction', ondelete='cascade')

    def _get_value(self):
        for r in self:
            r.predict_value = r.value * 100
