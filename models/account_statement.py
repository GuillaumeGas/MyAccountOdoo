# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AccountStatement(models.Model):
    _name = 'account.account_statement'

    name = fields.Char(string="Name", required=True)
    account_id = fields.Many2one('account.account', string="Account", required=True)
    bank_statement_id = fields.Many2one('account.bank_statement')
    transaction_ids = fields.One2many('account.transaction', 'account_statement_id')

    @api.onchange('account_id')
    def change_name(self):
        if self.account_id:
            self.name = self.account_id.name

    @api.multi
    def open_account_statement(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.transaction',
            'target': 'current',
            'domain': [('account_statement_id', '=', self.id)]
        }
