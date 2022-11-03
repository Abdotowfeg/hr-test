from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class HREmployeePromotion(models.Model):
    _name = 'hr.employee.promotion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'HR Employee Promotion'

    name = fields.Char(default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    employee_no = fields.Char(related='employee_id.employee_no', string='Employment ID')
    current_job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    join_date = fields.Date(related='employee_id.join_date', string='Joint Date')
    manager_id = fields.Many2one('hr.employee', string='Manager', readonly=True)
    current_department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('approve', 'Approved'),
                              ('cancel', 'Cancelled'), ('refuse', 'Refused')], string='Status', default='draft')
    contract_id = fields.Many2one('hr.contract', string='Contract', readonly=True)
    salary = fields.Monetary(string='Salary', related='contract_id.wage')
    request_date = fields.Date(string='Date', default=fields.Date.today())
    effective_date = fields.Date(string='Effective Date', readonly=1)
    new_manager_id = fields.Many2one('hr.employee', string='Manager')
    new_department_id = fields.Many2one('hr.department', string='Department')
    new_contract_id = fields.Many2one('hr.contract', string='Contract')
    new_salary = fields.Float(string='Salary')
    new_job_id = fields.Many2one('hr.job', string='Job Position')
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', compute='_compute_company', store=True, readonly=False,
                                 default=lambda self: self.env.company, required=True)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    image_128 = fields.Image(related='employee_id.image_128')
    image_1920 = fields.Image(related='employee_id.image_1920')
    avatar_128 = fields.Image(related='employee_id.avatar_128')
    avatar_1920 = fields.Image(related='employee_id.avatar_1920')
    promotion_url = fields.Char('URL', compute='get_url')

    @api.onchange('employee_id')
    def onchange_employee(self):
        self.current_job_id = self.employee_id.job_id
        self.current_department_id = self.employee_id.department_id
        self.manager_id = self.employee_id.parent_id
        self.contract_id = self.employee_id.contract_id

    def get_url(self):
        for record in self:
            ir_param = self.env['ir.config_parameter'].sudo()
            base_url = ir_param.get_param('web.base.url')
            action_id = self.env.ref('hr_employee_promotion.action_employee_promotion').id
            menu_id = self.env.ref('hr_employee_promotion.menu_view_probation_evaluation').id
            if base_url:
                base_url += '/web#id=%s&action=%s&model=%s&view_type=form&cids=&menu_id=%s' % (
                    record.id, action_id, 'hr.employee.promotion', menu_id)
            record.promotion_url = base_url

    @api.depends('employee_id')
    def _compute_company(self):
        for record in self.filtered('employee_id'):
            record.company_id = record.employee_id.company_id

    @api.model
    def create(self, values):
        if not values.get('name') or values['name'] == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('employee.promotion')
        return super(HREmployeePromotion, self).create(values)

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can't delete record not in draft state"))
        return super(HREmployeePromotion, self).unlink()

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_approve(self):
        self.write({'state': 'approve',
                    'effective_date': fields.Date.today()})
        self.employee_info_update()
        self._email_notification()

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_refuse(self):
        self.write({'state': 'refuse'})

    def _email_notification(self):
        template_id = self.env.ref('hr_employee_promotion.employee_promotion_mail_template')
        mtp = self.env['mail.template']
        template_id = mtp.browse(template_id.id)
        if self.employee_id.work_email or self.employee_id.user_id.partner_id.email:
            email_values = {
                'email_from': self.env.user.partner_id.email or self.company_id.email,
            }
            template_id.send_mail(self.id, force_send=True, email_values=email_values)

    def employee_info_update(self):
        for record in self:
            record.employee_id.job_id = record.new_job_id or record.current_job_id
            record.employee_id.department_id = record.new_department_id or record.current_department_id
            record.employee_id.parent_id = record.new_manager_id or record.manager_id
            record.employee_id.contract_id = record.new_contract_id or record.contract_id
            record.new_contract_id.wage = record.salary or record.new_salary


