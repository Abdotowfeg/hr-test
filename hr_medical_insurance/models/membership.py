# -*- coding: utf-8 -*-
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class InsuranceMembership(models.Model):
    """"""
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name = 'insurance.membership'
    _rec_name = 'employee_id'
    _description = "Insurance Membership"

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('expire', 'Expired')],
                             default='draft', string='State')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id, store=True)
    membership_type = fields.Selection([('employee', 'Employee'), ('family_member', 'Family Member')],
                                       string='Membership Type', default='employee')
    employee_id = fields.Many2one('hr.employee', string='Agent')
    family_id = fields.Many2one('hr.family', string='Agent')
    policy_id = fields.Many2one('insurance.policy', string='Policy')
    insurance_company_id = fields.Many2one("res.partner", related="policy_id.insurance_company_id")
    start_date = fields.Date(string="Start Date", related="policy_id.start_date")
    end_date = fields.Date(string="End Date", related="policy_id.end_date")
    allowed_class_id = fields.Many2one("insurance.class", string="Allowed Class")
    allowed_class_amount = fields.Float(string="Allowed Class Amount")
    selected_class_id = fields.Many2one("insurance.class", string="Selected Class")
    selected_class_amount = fields.Float(string="Selected Class Amount")
    amount_difference = fields.Monetary(string='Amount Difference', compute="_get_amount_difference")
    currency_id = fields.Many2one('res.currency', string='Currency', related="policy_id.currency_id")
    loan_count = fields.Integer(string="Loan", default=1)
    loan_id = fields.Many2one('hr.loan', string='Insurance Deficits')

    @api.onchange('policy_id')
    def _get_confirmed_policy(self):
        for rec in self:
            policies = self.env['insurance.policy'].search([('state', '=', 'bill')]).mapped('id')
            return {'domain': {'policy_id': [('id', 'in', policies)]}}

    @api.onchange('policy_id')
    def _get_allowed_class(self):
        for rec in self:
            class_ids = rec.policy_id.policy_class_ids.mapped('class_id.id')
            return {'domain': {'allowed_class_id': [('id', 'in', class_ids)]},
                    'value': {'allowed_class_id': class_ids[0] if len(class_ids) > 0 else None}}

    @api.onchange('policy_id')
    def _get_selected_class(self):
        for rec in self:
            class_ids = rec.policy_id.policy_class_ids.mapped('class_id.id')
            return {'domain': {'selected_class_id': [('id', 'in', class_ids)]},
                    'value': {'selected_class_id': class_ids[0] if len(class_ids) > 0 else None}}

    @api.onchange('policy_id', 'allowed_class_id','selected_class_id')
    def _get_amounts(self):
        # self.allowed_class_amount = 0.0
        # self.selected_class_amount = 0.0
        if self.allowed_class_id:
            self.allowed_class_amount = self.env['insurance.policy.class'].search([('class_id', '=', self.allowed_class_id.id),('policy_id', '=', self.policy_id.id)]).amount
        if self.selected_class_id:
            self.selected_class_amount = self.env['insurance.policy.class'].search([('class_id', '=', self.selected_class_id.id),('policy_id', '=', self.policy_id.id)]).amount


    def _get_amount_difference(self):
        self.amount_difference = self.selected_class_amount - self.allowed_class_amount

    def action_confirm(self):
        self.state = 'confirm'

    def action_create_loan(self):
        loan_obj = self.env['hr.loan']

        if self.amount_difference > 0:
            loan_id = loan_obj.create({
                "name": _("{} - Insurance Difference Amount".format(self.employee_id.name or self.family_id.employee_id.name)),
                "date": fields.Date.today(),
                "employee_id": self.employee_id.id or self.family_id.employee_id.id,
                "company_id": self.company_id.id,
                "currency_id": self.currency_id.id,
                "loan_amount": self.amount_difference,
                "state": "draft",
            })
            self.loan_id = loan_id.id

    def action_draft(self):
        self.state = 'draft'

    def action_view_loan(self):
        loan_obj = self.env.ref('hr_employee_loan.hr_loan_form_view')
        return {'name': _("{} Membership Difference").format(self.employee_id.name or self.family_id.employee_id.name),
                'view_mode': 'form',
                'res_model': 'hr.loan',
                'view_id': loan_obj.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': self.loan_id.id,
                'context': {}}
