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
            r.predict_value = r.account_id.value
            invalidated_transac = self.env['account.prediction'].search(
                [('validated', '=', False)])
            for transac in invalidated_transac:
                if (fields.Date.from_string(transac.date) < fields.Date.from_string(r.date)):
                    r.predict_value += transac.value
            if (not r.validated):
                r.predict_value += r.value
