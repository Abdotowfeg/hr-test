# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Contract Extension'


    schedule_pay = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semi-annually', 'Semi-annually'),
        ('annually', 'Annually'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('bi-monthly', 'Bi-monthly'),
    ], string='Scheduled Pay', index=True, default='monthly',
    help="Defines the frequency of the wage payment.")
    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')


    def compute_allowance(self, payslip, code=None):
        result= 0.0
        for rec in payslip.contract_id.attribute_value_ids:
            if rec.attribute_id.code == code:
                result = rec.value
        return result

    def compute_deduction(self, payslip, code=None):
        result= 0.0
        for rec in payslip.contract_id.attribute_value_ids:
            if rec.attribute_id.code == code:
                result = rec.value
        return float(result)

    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by hierachy (parent=False first,
                 then first level children and so on) and without duplicata
        """
        structures = self.mapped('struct_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))



