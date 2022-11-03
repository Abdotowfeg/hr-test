from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning as UserError


class HrDeputations(models.Model):
    _name = 'hr.deputations'
    _description = 'Employee Business Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char(string='Name', default='New')
    employee_no = fields.Char(related='employee_id.employee_no', string='Employee No')

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
    department_id = fields.Many2one('hr.department', string='Department', related='employee_id.department_id',
                                    store=True)
    job_id = fields.Many2one('hr.job', string='Job Position', related='employee_id.job_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.company)

    country_id = fields.Many2one('res.country', string='Country', readonly=True,
                                 states={'draft': [('readonly', False)]})
    destination_country = fields.Many2one('res.country', string='Destination Country', readonly=True,
                                          states={'draft': [('readonly', False)]})
    from_city = fields.Many2one('res.city', string='From City', readonly=True,
                                states={'draft': [('readonly', False)]})
    to_city = fields.Many2one('res.city', string='To City', readonly=True,
                              states={'draft': [('readonly', False)]})

    deputation_type = fields.Selection([('internal', 'Internal'), ('external', 'External')], string='Deputation Type',
                                       default='internal', readonly=True,
                                       states={'draft': [('readonly', False)]})
    request_date = fields.Date('Request Date', default=fields.Datetime.now, readonly=True,
                               states={'draft': [('readonly', False)]})
    end_date = fields.Date('End Date', readonly=True,
                           states={'draft': [('readonly', False)]})
    from_date = fields.Date('From Date', readonly=True,
                            states={'draft': [('readonly', False)]})
    to_date = fields.Date('To Date', readonly=True,
                          states={'draft': [('readonly', False)]})
    duration = fields.Integer(string='Duration', compute='_compute_duration')
    days_before = fields.Integer(string='Days Before', readonly=True,
                                 states={'draft': [('readonly', False)]})
    days_after = fields.Integer(string='Days after', readonly=True,
                                states={'draft': [('readonly', False)]})

    travel_by = fields.Selection([('land', 'By Land'), ('air', 'By Air')], string='Travel By', readonly=True,
                                 states={'draft': [('readonly', False)]}, required=True)
    housing_by = fields.Selection(
        [('company', 'By Company'), ('employee', 'Cash On Hand'), ('half_day', 'Half Day')], string='Hotel Reservation',
        readonly=True, required=True,
        states={'draft': [('readonly', False)]})
    tansp_cost = fields.Selection([('company', 'By Company'), ('employee', 'Cash On Hand')],
                                  string='Transportation', readonly=True, required=True,
                                  states={'draft': [('readonly', False)]})

    description = fields.Text(string='Description')
    end_report = fields.Text(string='Task Report')

    basic_allownce = fields.Float('Basic Allowance', compute="_compute_allownces", store=True)
    other_allownce = fields.Float('Other Allowance', compute="_compute_allownce_amount")
    total_amount = fields.Float('Total Amount', compute="_compute_allownce_amount")

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('approve', 'Approved'), ('cancel', 'Canceled')],
                             string='Status', required=True, default='draft', track_visibility='onchange')

    deputation_account = fields.Many2one('account.analytic.account', string="Analytic Account")
    line_ids = fields.One2many('hr.deputations.allownce.lines', 'deputation_id',
                               string='Deputation Lines', tracking=True, track_visibility='onchange', readonly=True,
                               states={'draft': [('readonly', False)]})
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='Number of Attachments')
    payment_ids = fields.One2many('account.payment', 'deputation_id')
    payment_count = fields.Integer(string='Payment count', default=0, compute='count_payments')
    ticket_count = fields.Integer(string='Tickets count', default=0, compute='count_tickets')

    @api.depends('payment_ids')
    def count_payments(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    def count_tickets(self):
        for rec in self:
            rec.ticket_count = len(self.env['hr.ticketing'].search([('deputation_id', '=', self.id)]))

    @api.onchange('duration')
    def onchange_duration(self):
        self._compute_allownce_amount()
        self._onchange_to_city()

    @api.onchange('to_city')
    def _onchange_to_city(self):
        for rec in self:
            rec.line_ids = None
            lines = []
            basic_allow = self.env['hr.deputations.allownce'].search([('id', '>=', 0)])
            for basic in basic_allow:

                if rec.to_city.country_id in basic.counter_group.country_ids:
                    for allownce_type in basic.other_allownce_ids:
                        amount = 0.0
                        if allownce_type.amount_type == 'amount':
                            amount = allownce_type.amount
                        if allownce_type.amount_type == 'percentage':
                            if allownce_type.percentage_type == 'basic':
                                amount = (self.employee_id.contract_id.wage * allownce_type.percentage) / 100
                            if allownce_type.percentage_type == 'allownce':
                                amount = (self.basic_allownce * allownce_type.percentage) / 100

                        line_vals = {'allownce_type': allownce_type.id,
                                     'amount': amount,
                                     }
                        lines.append((0, 0, line_vals))
            rec.line_ids = lines

    @api.depends('employee_id.job_id', 'deputation_type', 'duration', 'to_city.country_id', 'days_after', 'days_before')
    def _compute_allownces(self):
        for rec in self:
            basic_allow = self.env['hr.deputations.allownce'].search([('id', '>=', 0)])
            for basic in basic_allow:

                if rec.to_city.country_id in basic.counter_group.country_ids:
                    for line in basic.line_ids:
                        if rec.job_id in line.job_ids:
                            days_no = rec.duration + rec.days_before + rec.days_after
                            rec.basic_allownce = line.amount * days_no

            rec._onchange_to_city()

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("You can delete record in draft state only!"))
        return super(HrDeputations, self).unlink()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id and not self.employee_id.job_id:
            raise ValidationError(_("Please Set job Position for this employee!!"))

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'hr.deputations'), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for dept in self:
            dept.attachment_number = attachment.get(dept._origin.id, 0)

    def action_get_attachment_view(self):
        self.ensure_one()
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_attachment')
        res['domain'] = [('res_model', '=', 'hr.deputations'), ('res_id', 'in', self.ids)]
        res['context'] = {'default_res_model': 'hr.deputations', 'default_res_id': self.id}
        return res

    def attach_document(self, **kwargs):
        pass

    @api.depends('line_ids', 'basic_allownce')
    def _compute_allownce_amount(self):
        for rec in self:
            total = 0.0
            for line in rec.line_ids:
                total += line.amount
            rec.other_allownce = total

            total_amount = rec.other_allownce + rec.basic_allownce

            rec.total_amount = total_amount

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id.partner_id.country_id:
            self.write({'country_id': self.company_id.partner_id.country_id,
                        'destination_country': self.company_id.partner_id.country_id})
        if self.company_id.partner_id.city_id:
            self.write({'from_city': self.company_id.partner_id.city_id})

        deputation_account = self.env['ir.config_parameter'].get_param('hr_deputation.hr_deputation_account')
        acc = int(deputation_account)
        self.write({'deputation_account': acc})

    @api.onchange('deputation_type')
    def onchange_deputation_type(self):
        if self.deputation_type == 'external':
            self.write({'destination_country': False, 'to_city': False})
        if self.deputation_type == 'internal':
            self.onchange_company_id()

    def action_confirm(self):
        seq = self.env['ir.sequence'].next_by_code('hr.deputations')

        self.write({'state': 'confirm', 'name': seq})

    def action_approve(self):
        self.write({'state': 'approve'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.depends('from_date', 'to_date')
    def _compute_duration(self):
        for record in self:
            if record.from_date and record.to_date:
                record.duration = (record.to_date - record.from_date).days
            else:
                record.duration = 0

    def action_register_payment(self):
        action = self.env.ref('account.action_account_payments').read()[0]
        view_id = self.env.ref('account.view_account_payment_form').id
        action.update({'views': [(view_id, 'form')], })
        action['context'] = {
            'default_partner_id': self.employee_id.address_home_id.id,
            'default_payment_type': 'outbound',
            'default_amount': self.total_amount,
            'default_deputation_id': self.id,
            'default_journal_id': 11, 'default_ref': 'Business Trip %s' % self.name
        }
        return action

    def action_create_ticket(self):

        return {
            'name': _('Book Ticket'),
            'res_model': 'hr.ticketing',
            'view_mode': 'form',
            'context': {
                'default_employee_id': self.employee_id.id,
                'default_deputation_id': self.id

            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def action_payment_view(self):
        pay_obj = self.env.ref('account.view_account_payment_form')
        paymemt = self.env['account.payment'].search_count([('deputation_id', '=', self.id)])
        payment_id = self.env['account.payment'].search([('deputation_id', '=', self.id)])
        if paymemt == 1:
            return {'name': _("Deputation Payment"),
                    'view_mode': 'form',
                    'res_model': 'account.payment',
                    'view_id': pay_obj.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': payment_id.id,
                    'context': {}}

    def action_ticket_view(self):
        ticket_obj = self.env.ref('hr_deputation.hr_ticketing_form')
        ticket = self.env['hr.ticketing'].search_count([('deputation_id', '=', self.id)])
        ticket_id = self.env['hr.ticketing'].search([('deputation_id', '=', self.id)])
        if ticket == 1:
            return {'name': _("Deputation Ticket"),
                    'view_mode': 'form',
                    'res_model': 'hr.ticketing',
                    'view_id': ticket_obj.id,
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'res_id': ticket_id.id,
                    'context': {}}


class AccountPayment(models.Model):
    _inherit = "account.payment"

    deputation_id = fields.Many2one('hr.deputations',
                                    string="Deputation", store=True)


class HrDeputationLines(models.Model):
    _name = 'hr.deputations.allownce.lines'

    _inherit = ['mail.thread']

    allownce_type = fields.Many2one('hr.deput.other.allownce')

    deputation_id = fields.Many2one('hr.deputations', 'Deputation')

    amount = fields.Float('Amount')

    @api.onchange('allownce_type')
    def onchange_allownce_type(self):

        if self.allownce_type.amount_type == 'amount':
            self.amount = self.allownce_type.amount
        if self.allownce_type.amount_type == 'percentage':
            if self.allownce_type.percentage_type == 'basic':
                amount = (self.deputation_id.employee_id.contract_id.wage * self.allownce_type.percentage) / 100
                self.amount = amount
            if self.allownce_type.percentage_type == 'allownce':
                amount = (self.deputation_id.basic_allownce * self.allownce_type.percentage) / 100
