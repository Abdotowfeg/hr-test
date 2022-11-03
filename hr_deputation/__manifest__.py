
{

    'name': 'Hr Deputation Management(Saudi)',
    'version': '1.0',
    'category': 'Human Resources/Employees',

    'author': '',
    'depends': ['base','hr_employee_extension','account', 'base_address_city'],
    'data': [
        'security/hr_deputation_security.xml',
        'security/ir.model.access.csv',
        'views/sequence.xml',
        'wizard/deputation_summary_wizard.xml',
        'views/deputation_request_view.xml',
        'views/tickiting_view.xml',
        'views/configuration_view.xml',
        'views/basic_deptuation_allownce.xml',
        'views/other_deptuation_allownce.xml',
        'views/country_groups.xml',


    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
