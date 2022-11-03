# -*- coding: utf-8 -*-
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustodyRequest(models.Model):
    """"""
    _name = 'custody.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'asset_id'
    _description = "Custody Request"

    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('approve', 'Approved'),
                              ('assign', 'Assigned'), ('return', 'Returned'), ('refuse', 'Refused'),
                              ('cancel', 'Cancelled')], string='Status', default='draft', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one("hr.department", related="employee_id.department_id", string="Department")
    manager_id = fields.Many2one("hr.employee", related="employee_id.parent_id", string="Manager")
    employee_job = fields.Many2one("hr.job", related="employee_id.job_id", string="Job Position")
    employee_no = fields.Char(related="employee_id.employee_no", string="Employee No")
    asset_id = fields.Many2one('account.asset', domain=[('asset_type', '=', 'purchase'), ('state', '!=', 'model'),
                                                        ('state', '=', 'open'), ('employee_id', '=', False)],
                               string="Asset", copy=False)
    custody_asset_id = fields.Many2one('custody.asset', string="Custody Asset", copy=False)
    request_date = fields.Date(string="Request Date", default=fields.Date.today())
    assign_date = fields.Date(string="Assign Date", copy=False)
    return_date = fields.Date(string="Return Date", copy=False)
    desc = fields.Text(string="Description")

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'

    def action_draft(self):
        self.state = 'draft'

    def action_assign(self):
        old_custody_asset = self.env['custody.asset'].search([('asset_id', '=', self.asset_id.id)])
        if not old_custody_asset:
            new_custody_asset = self.env['custody.asset'].create({
                "asset_id": self.asset_id.id,
            })
            self.custody_asset_id = new_custody_asset.id
        else:
            self.custody_asset_id = old_custody_asset.id
        self.asset_id.employee_id = self.employee_id.id
        self.assign_date = fields.Date.today()
        self.state = 'assign'

    def action_return(self):
        self.asset_id.employee_id = False
        self.return_date = fields.Date.today()
        self.state = 'return'

    def action_refuse(self):
        self.state = 'refuse'

    def action_cancel(self):
        self.state = 'cancel'


class CustodyAsset(models.Model):
    """"""
    _name = 'custody.asset'
    _rec_name = 'asset_id'
    _description = "Custody Asset"

    asset_id = fields.Many2one('account.asset', string="Asset")
    asset_model_id = fields.Many2one('account.asset', string="Asset Model", related="asset_id.model_id")
    custody_request_ids = fields.One2many('custody.request', 'custody_asset_id', string="Custodies")


class AccountAsset(models.Model):
    """"""
    _inherit = 'account.asset'

    custody = fields.Boolean(string="Custody", default=False)
    employee_id = fields.Many2one('hr.employee', string="Employee")


class HrEmployee(models.Model):
    """"""
    _inherit = 'hr.employee'

    custody_count = fields.Integer(string="Custodies", compute="_get_custody_count")

    def _get_custody_count(self):
        """"""
        self.custody_count = self.env["custody.request"].search_count([('employee_id', '=', self.id),
                                                                       ('state', '=', "assign")])

    def action_get_custody(self):
        # This function is action to view employee custodies
        custodies = self.env["custody.request"].search_count([('employee_id', '=', self.id),
                                                              ('state', '=', "assign")])
        return {
            'name': '{} Custodies'.format(self.name),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'custody.request',
            'domain': [('employee_id', 'in', custodies.mapped('employee_id.id'))]
        }
