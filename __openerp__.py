# -*- coding: utf-8 -*-
{
    'name': 'MyAccount',
    'version': '0.2',
    'category': 'custom',
    'author': 'Guillaume Gas',
    'website': 'https://guillaume.gas28.net',
    'depends': [
        'base',
        'email_template',
    ],
    'data': [
        'data/email_template.xml',
        'data/cron.xml',
        'views/account.xml',
        'views/transaction.xml',
        'views/category.xml',
        'views/prediction.xml',
        'views/menu.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'licence': 'GPL',
}
