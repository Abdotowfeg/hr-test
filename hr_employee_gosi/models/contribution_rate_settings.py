# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _


class ContributionRateSetting(models.Model):
    _name = 'gosi.contribution.setting'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    company_contribution_ids = fields.One2many('gosi.company.contribution', 'parent_id')
    employee_contribution_ids = fields.One2many('gosi.employee.contribution', 'parent_id')


class CompanyContribution(models.Model):
    _name = 'gosi.company.contribution'

    name = fields.Char(string='Name', required=True)
    region_type = fields.Selection([('all', 'All Employees'), ('saudi', 'Saudi'),
                                    ('non-saudi', 'Non-Saudi')], string='Type', required=True)
    percentage = fields.Float(string='Percentage', required=True)
    parent_id = fields.Many2one('gosi.contribution.setting', required=True)


class EmployeeContribution(models.Model):
    _name = 'gosi.employee.contribution'

    name = fields.Char(string='Name', required=True)
    region_type = fields.Selection([('all', 'All Employees'), ('saudi', 'Saudi'),
                                    ('non-saudi', 'Non-Saudi')], string='Type', required=True)
    percentage = fields.Float(string='Percentage', required=True)
    parent_id = fields.Many2one('gosi.contribution.setting', required=True)