# -*- coding: utf-8 -*-
{
    'name': "Bookstore",

    'summary': """
        Bookstore""",

    'description': """
        Bookstore
    """,

    'category': 'Uncategorized',
    'version': '0.1',

    'author': "Bookstore",

    # any module necessary for this one to work correctly
    'depends': ['base','deltatech_widget_badge'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/base.xml',
        'views/book.xml',
        'views/author.xml',
        'views/employee.xml',
        'views/supplier.xml',
        'views/sale_order.xml',
        'views/sale_order_line.xml',
        'views/sale_order_report.xml',
        'views/purchase_order.xml',
        'views/purchase_order_line.xml',
        'views/purchase_order_report.xml',
        'views/stock_transfer.xml',
        'views/stock_transfer_line.xml',
        'views/stock_transfer_report.xml',
    ],
}
