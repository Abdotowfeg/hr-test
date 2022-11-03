# -*- coding:utf-8 -*-

from odoo import api, fields, models


class HrContract(models.Model):
    """
    allows to configure different Salary structure
    """
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    hra = fields.Monetary(string='Housing Allowance', tracking=True)
    transport_allowance = fields.Monetary(string="Transportation Allowance", tracking=True)
    other_allowance = fields.Monetary(string="Other Allowance", help="Other allowances")