# -*- coding: utf-8 -*-
from openerp import models, fields


class Category (models.Model):
    _name = 'account.category'

    _sql_constraint = [('name_unique', 'UNIQUE(name)', 'The name must be unique')]

    name = fields.Char(string="Category", required=True)
   