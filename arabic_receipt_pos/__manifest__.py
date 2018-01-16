# -*- coding: utf-8 -*-
{
    'name': "Arabic POS Receipt",

    'summary': """ This module enables arabic printing for POS receipt from Right to Left (RTL) Using PosBox.
        """,

    'description': """
        
    """,

    'author': "Abdelmalik Yousif",
    'website': "abdelmalik19930@gmail.com",
    'category': 'Generic Modules',
    'version': '1.0',
    'price': 300.0,
    'currency': 'EUR',
    'depends': ['point_of_sale'],


    'data': [
        'views/malik.xml',
        'views/malik_v.xml',
    ],
    'images': [
        'static/description/pos_receipt.png',
    ],

    'demo': [
        #'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
