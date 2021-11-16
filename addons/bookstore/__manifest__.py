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
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/base.xml',
        'views/book.xml',
        'views/author.xml',
        'views/employee.xml',
        'views/supplier.xml',
    ],
}
