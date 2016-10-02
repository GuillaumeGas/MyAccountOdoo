# -*- coding: utf-8 -*-
from openerp import models, fields


class Account (models.Model):
    _name = 'account.account'

    name = fields.Char(string="Compte", required=True)
    value = fields.Float(string="Solde", default=0.0)

    transaction_ids = fields.One2many('account.transaction', ondelete='cascade')
