"""
Developed on Sept 20, 2022

@author: EGN. Hassan Abdallah
"""
from odoo import models, fields, api, _

import odoo.exceptions
from odoo.exceptions import UserError


class EndOfServiceReason(models.Model):
    _name = 'hr.end_of_service.reason'
    _description = _name
    _order = 'name'

    name = fields.Char(required=True, translate=True)
    code = fields.Char()
    eos_rule_ids = fields.One2many('eos.reason.rules', 'reason_id')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Name must be unique!')
    ]


class EndOfServiceRules(models.Model):
    _name = 'eos.reason.rules'

    name = fields.Char(string="Name", required=True, translate=True)
    active = fields.Boolean(default=True)
    from_year = fields.Float(string="From Year")
    to_year = fields.Float(string="To Year")
    yr_from_flag = fields.Boolean(compute="_compute_yr_field_required",
                                  store=True)
    yr_to_flag = fields.Boolean(compute="_compute_yr_field_required",
                                store=True)
    reason_id = fields.Many2one('hr.end_of_service.reason')
    company_id = fields.Many2one('res.company', 'Company', required=True, help="Company",
                                 index=True,
                                 default=lambda self: self.env.company)
    percentage = fields.Float(default=1)

    @api.onchange('from_year', 'to_year')
    def onchange_year(self):
        """ Function to check year configuration """
        if self.from_year and self.to_year:
            if not self.from_year < self.to_year:
                raise UserError(_("Invalid year configuration!"))

    @api.depends('from_year', 'to_year')
    def _compute_yr_field_required(self):
        """ Compute year from and to required """
        for rec in self:
            rec.yr_from_flag = True if not rec.to_year else False
            rec.yr_to_flag = True if not rec.from_year else False
