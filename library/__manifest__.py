# -*- coding: utf-8 -*-
{
    'name': "图书馆",
    'summary': "图书馆",
    'description': "图书馆",
    'author': "www.mypscloud.com",
    'website': 'https://www.mypscloud.com/',
    'category': 'train',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/book.xml',
        'views/rent.xml',
        'views/views.xml',
        'data/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
