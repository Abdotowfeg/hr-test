'''
Created on April 26, 2022

@author: Mutwkil Faisal
'''
from odoo import models, fields

class HREmployee (models.Model):
    _inherit = 'hr.employee.public'
        
    employee_no = fields.Char('Employee Company ID', readonly=True) 
