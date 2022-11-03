'''
Created on March 25, 2022

@author: Mutwkil Faisal
'''
from odoo import models, fields


class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    calc_type = fields.Selection([('work', 'Working Days'), ('calendar', 'Calendar Days')], string='Calculation Type',
                                 required=True, default='work')
    attachment_required = fields.Boolean('Attachment Required')
    for_specific_gender = fields.Boolean('For Specific Gender')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Type')
    is_annual = fields.Boolean('Annual Leave')
    allow_negative = fields.Boolean('Allow Negative')
    negative_limit = fields.Integer('Limit')
