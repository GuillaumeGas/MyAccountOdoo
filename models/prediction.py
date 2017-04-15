# -*- coding: utf-8 -*-
from openerp import models, fields
import logging

_logger = logging.getLogger(__name__)


class Prediction (models.Model):
    _name = 'account.prediction'
    _inherits = {'account.transaction': 'transaction_id'}

    predict_value = fields.Float(string="Value", compute='_get_value')
    start_date = fields.Date(string="Start date", default=fields.Date.today())
  
    transaction_id = fields.Many2one('account.transaction', ondelete='cascade')

    def _get_value(self):
        for r in self:
            r_date = fields.Date.from_string(r.date)
            transac = self.env['account.prediction'].search([('transaction_id.account_id.main_account','=','true')])
            value = 0.0
            for t in transac:
                t_date = fields.Date.from_string(t.date)
                if (t_date <= r_date):
                    value += t.value
            r.predict_value = round(value, 2)
           
