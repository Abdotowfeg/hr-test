'''
Created on April 26, 2022

@author: Mutwkil Faisal
'''
from odoo import models, fields, api

class HREmployee (models.Model):
    _inherit = 'hr.employee'

    def _get_default_employee_id_method(self):
        return self.env['ir.config_parameter'].sudo().get_param('lm_hr_employee.employee_id_option')
        
    employee_no = fields.Char('Employee ID', copy = False)
    arabic_name = fields.Char('Employee arabic name', copy = False)
    join_date = fields.Date('Joining date')
    identification_end_date = fields.Date('ID End Date')
    passport_end_date = fields.Date('Passport Expiry Date')
    iqama_id = fields.Char('Iqama Number')
    iqama_end_date = fields.Date('Iqama Expiry Date')
    border_no = fields.Char('Border Number')
    employee_id_option = fields.Selection( [('manual', 'Manual Entry'),('auto', 'Auto Generation')],string='Employee ID Generation Method',
                                           default = lambda self: self._get_default_employee_id_method())
    country_code  = fields.Char(related='country_id.code')


    @api.model
    def create(self,vals):
        result = super(HREmployee,self).create(vals)
        employee_id_option = self.env['ir.config_parameter'].sudo().get_param('lm_hr_employee.employee_id_option')
        if employee_id_option=='auto':
            result['employee_no'] = self.env['ir.sequence'].next_by_code('hr.employee.id')
        return result



    _sql_constraints= [
            ('employee_no_unqiue', 'unique(company_id, employee_no)', 'Employee Company ID must be unique!')
    ]    
                
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        
        search_limit = limit
        sort_by_search_input = self.env['ir.config_parameter'].sudo().get_param('employee_name_search_sort_by_search_input') == 'True'
        if sort_by_search_input:
            search_limit = None
        
        if not recs:
            recs = self.search([('name', operator, name)] + args, limit = search_limit)
        
        if name and sort_by_search_input:
            recs = recs.sorted(key = lambda rec : (1 if rec.name.lower().startswith(name.lower()) else 2, rec.name))
            
        recs = recs[:limit]    
        
        return recs.name_get()
