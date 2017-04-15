# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Account (models.Model):
    _name = 'account.account'

    name = fields.Char(string="Name", required=True)
    value = fields.Float(string="Value", compute='_get_value')
    main_account = fields.Boolean(string="Main account", default=False)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, ondelete='cascade')

    transaction_ids = fields.One2many(
        'account.transaction', 'account_id', string="Transactions")

    @api.multi
    def _get_value(self):
        for r in self:
            value = 0.0
            for trans in r.transaction_ids:
                if trans.validated:
                    value += trans.value
            r.value = value
