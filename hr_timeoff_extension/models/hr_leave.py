'''
Created on March 25, 2022

@author: Mutwkil Faisal
'''
from odoo import models, fields, api, _
from odoo.addons.resource.models.resource import HOURS_PER_DAY
from odoo.exceptions import ValidationError


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    number = fields.Char(index=True, readonly=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Supporting Documents')
    balance = fields.Float(compute="_compute_employee_balance", store=True)

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        for vals in vals_list:
            employee = self.env['hr.employee'].browse(vals['employee_id'])
            # vals['number'] = self.env['ir.sequence'].with_company(employee.company_id).next_by_code(self._name)
            vals['number'] = self.env['ir.sequence'].next_by_code(self._name)
        return super(HolidaysRequest, self).create(vals_list)

    def _get_number_of_days(self, date_from, date_to, employee_id):
        if self.holiday_status_id.calc_type == 'calendar':
            days = (date_to - date_from).days + 1
            return {'days': days, 'hours': HOURS_PER_DAY * days}
        return super(HolidaysRequest, self)._get_number_of_days(date_from, date_to, employee_id)

    @api.depends('employee_id', 'holiday_status_id')
    def _compute_employee_balance(self):
        for rec in self:
            balance = self.env['hr.leave.balance'].search(
                [('employee_id', '=', rec.employee_id.id), ('leave_type', '=', rec.holiday_status_id.id)])
            rec.balance = balance.remaining
            # rec.balance = rec.employee_id.allocation_count - rec.employee_id.allocation_used_count

    @api.constrains('state', 'holiday_status_id', 'attachment_ids')
    def _check_attachment(self):
        for record in self:
            if record.state not in ['draft', 'cancel', 'refuse'] and record.holiday_status_id.attachment_required \
                    and not record.attachment_ids:
                raise ValidationError(_('You cannot send the leave request without attaching a document.'))

    @api.constrains('employee_id', 'holiday_status_id', 'start_date', 'end_date')
    def _check_negative_leave(self):
        for record in self:
            if record.state not in ['draft', 'cancel',
                                    'refuse'] and record.holiday_status_id.allow_negative:
                if 0 < record.holiday_status_id.negative_limit < record.number_of_days:
                    raise ValidationError(_('You cannot take a(an) %s leave more than %s day(s).' % (
                        record.holiday_status_id.name, record.holiday_status_id.negative_limit)))

    # @api.constrains('state','holiday_status_id')
    # def _check_attachment(self):
    #     for record in self:
    #         if record.state not in ['draft', 'cancel', 'refuse'] and record.holiday_status_id.attachment_required:
    #             if not self.env['ir.attachment'].search([('res_model','=', self._name), ('res_id','=', record.id)], limit = 1):
    #                 raise ValidationError(_('You cannot send the leave request without attaching a document.'))

    @api.constrains('state', 'holiday_status_id')
    def _check_gender(self):
        for record in self:
            if record.state not in ['draft', 'cancel', 'refuse'] and record.holiday_status_id.for_specific_gender:
                if record.employee_id.gender != record.holiday_status_id.gender:
                    raise ValidationError(_('This Leave is not allowed for this gender.'))

#     @api.onchange('holiday_status_id')
#     def _onchange_holiday_status_id(self):
#         super(HolidaysRequest, self)._onchange_holiday_status_id()
#         self._onchange_leave_dates()
