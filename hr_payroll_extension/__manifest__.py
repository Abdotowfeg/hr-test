# -*- coding: utf-8 -*-
{
    'name': "Payroll Extension (Saudi)",

    'summary': """Customize payroll KSA bas""",

    'description': """
        Customize payroll KSA bas
    """,

    'author': "",
    'category': 'Human Resources/Payroll',
    'version': '15.0',

    'depends': ['hr_payroll', 'hr_contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_contract_views.xml',
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_data.xml'
    ],
    
}
