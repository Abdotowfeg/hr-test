# -*- coding: utf-8 -*-
{
    'name': 'HR Employee Promotions(Saudi)',
    'version': '15.0.0.0.0',
    'author': 'No-name',
    'company': 'No-name',
    'category': 'Human Resources/Promotion',
    'description': """This module helps you to track promotions applied to employees""",
    'summary': """This module helps you to track promotions applied to employees""",
    'depends': ['hr_employee_extension', 'hr_contract_extension'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/mail_template.xml',
        'views/employee_promotion.xml',
    ],
    'sequence': 21,
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
