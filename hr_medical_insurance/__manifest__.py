# -*- coding: utf-8 -*-
{
    'name': "HR Medical Insurance",

    'summary': """
        A module to manage hr medical insurance""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_employee_family','hr_employee_loan','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/policy_views.xml',
        'views/membership_views.xml',
        'views/res_config_settings.xml',
        'data/mail_data.xml',
    ],
}
