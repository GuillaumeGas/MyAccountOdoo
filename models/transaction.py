# -*- coding: utf-8 -*-
from openerp import models, fields, api
from urlparse import urljoin
from urllib import urlencode
import logging

_logger = logging.getLogger(__name__)


class Transaction (models.Model):
    _name = 'account.transaction'
    _order = 'date'

    name = fields.Char(string="Name", required=True)
    value = fields.Float(string="Value", required=True)
    date = fields.Date(string="Date", required=True, default=fields.Date.today())
    validated = fields.Boolean(string="Validated", default=True)

    account_id = fields.Many2one('account.account', string="Account",
                                 required=True, ondelete='cascade')
    account_statement_id = fields.Many2one('account.account_statement')
    category_id = fields.Many2one('account.category', string="Category",
                                  required=True, ondelete='set null')

    @api.model
    def create(self, values):
        if (values['validated']):
            account = self.env['account.account'].search([('id', '=', values['account_id'])])
            account.value += values['value']
        res = super(Transaction, self).create(values)
        self.env['account.prediction'].create(
            {'transaction_id': res.id, 'predict_value': res.value})
        return res

    @api.multi
    def write(self, values):
        if ('validated' in values):
            if (values['validated']):
                account = self.env['account.account'].search([('id', '=', self.account_id.id)])
                value = self.value
                if ('value' in values):
                    value = values['value']
                account.value += value
        if ('value' in values):
            if (('validated' in values and values['validated']) or
                    ('validated' not in values and self.validated)):
                transaction = self.env['account.transaction'].search([('id', '=', self.id)])
                self.account_id.value -= transaction.value
                self.account_id.value += values['value']
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

    @api.multi
    def get_url(self):
        url_base = self.env['ir.config_parameter'].get_param('web.base.url')
        imd = self.env['ir.model.data']
        menu_id = imd.get_object_reference('MyAccountOdoo', 'transaction_menu')
        action_id = imd.get_object_reference('MyAccountOdoo', 'transaction_action')

        if menu_id:
            menu_id = menu_id[1]
        if action_id:
            action_id = action_id[1]

        args = {}
        args['id'] = self.id
        args['view_type'] = 'form'
        args['model'] = 'account.transaction'
        args['menu_id'] = menu_id
        args['action'] = action_id

        res = urljoin(url_base, "web#%s" % urlencode(args))
        return res

    @api.model
    def cron_mail(self):
        not_validated = self.get_list_invalidated()
        nb_not_validated = len(not_validated)

        if nb_not_validated > 0:
            template = self.env['ir.model.data'].get_object(
                'MyAccountOdoo', 'email_myaccount')

            # tmp !
            template.email_to = "guillaume@gas-ntic.fr"
            template.send_mail(res_id=self.env['account.transaction'].search([], limit=1).id)

    def get_list_invalidated(self):
        invalidated_list = self.env['account.transaction'].search([('validated', '=', False)])
        res_list = []
        today = fields.Date.today()
        for transac in invalidated_list:
            if (fields.Date.from_string(transac.date) <= fields.Date.from_string(today)):
                res_list.append(transac)
        return res_list
