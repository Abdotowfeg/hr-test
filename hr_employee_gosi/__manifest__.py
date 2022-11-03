# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': "HR: GOSI Contribution (Saudi)",
    'summary': """HR GOSI Contribution""",
    'description': """
        By this module we can calculate GOSI of employee and can deduct the amount from employee payslip.
    """,
    'author': '',
    'category': 'Generic Modules/Human Resources',
    'version': '1.0',
    'depends': ['hr_employee_extension', 'hr_payroll_extension'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/hr_payroll_data.xml',
        'views/gosi_settings.xml',
        'views/hr_employee_gosi_view.xml',
        'views/hr_payroll_view.xml',
        'views/menu-items.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/employee_gosi_demo.xml',
    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
