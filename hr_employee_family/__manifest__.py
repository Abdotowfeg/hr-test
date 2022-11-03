# -*- coding: utf-8 -*-
{
    'name': "Employee Family(Saudi)",

    'summary': """
        Employee Family Members""",

    'description': """
        Employee Family Members
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_family.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
