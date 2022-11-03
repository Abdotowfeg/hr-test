# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def _include_gosi(self):
        for line in self:
            date_from = datetime.strptime(str(line.date_from), DEFAULT_SERVER_DATE_FORMAT)
            day_to = datetime.strptime(str(line.date_to), DEFAULT_SERVER_DATE_FORMAT)
            day_upto = date_from + relativedelta(day=25)
            last_date = day_to + relativedelta(months=+1, day=1, days=-1)
            if day_to == last_date and date_from < day_upto:
                line.include_gosi = True

    gosi_id = fields.Many2one('employee.gosi', related='employee_id.gosi_ids',
                              string='GOSI NO', readonly=True)
    include_gosi = fields.Boolean(compute='_include_gosi', string='Include GOSI in Payslip')


