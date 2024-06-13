from odoo import api, models,fields
from datetime import date
from dateutil.relativedelta import relativedelta


class EmployeeBirthdateFilter(models.TransientModel):
    _name = 'hr.employee.birthdate.filter.wizard'
    _inherit = ['mail.thread']

    from_date = fields.Date(string="From Date", required=True, default=date.today())
    to_date = fields.Date(string="To Date", required=True, default=date.today() + relativedelta(days=30))
    type = fields.Selection([('dob', 'Birthday'), ('wa', 'Work anniversary')], default="dob", required=True)

    def apply_filter(self):
        from_month = self.from_date.month
        from_day = self.from_date.day
        to_month = self.to_date.month
        to_day = self.to_date.day

        if self.type == 'dob':
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM birthday) * 100 + EXTRACT(DAY FROM birthday)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """
        else:
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM current_contract_start) * 100 + EXTRACT(DAY FROM current_contract_start)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """

        self.env.cr.execute(query, (from_month, from_day, to_month, to_day))
        employee_ids = [row[0] for row in self.env.cr.fetchall()]
        action = self.env.ref('hr.open_view_employee_list_my').read()[0]
        action['domain'] = [('id', 'in', employee_ids)]
        return action

    def upcoming_month(self):
        today = date.today()
        next_month = today + relativedelta(months=1)
        from_month = next_month.month
        from_day = 1
        to_month = next_month.month
        to_day = 31

        if self.type == 'dob':
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM birthday) * 100 + EXTRACT(DAY FROM birthday)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """
        else:
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM current_contract_start) * 100 + EXTRACT(DAY FROM current_contract_start)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """

        self.env.cr.execute(query, (from_month, from_day, to_month, to_day))
        employee_ids = [row[0] for row in self.env.cr.fetchall()]
        action = self.env.ref('hr.open_view_employee_list_my').read()[0]
        action['domain'] = [('id', 'in', employee_ids)]
        return action



    def current_month(self):
        today = date.today()


        from_month = today.month
        from_day = 1
        to_month = today.month
        to_day = 31

        if self.type == 'dob':
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM birthday) * 100 + EXTRACT(DAY FROM birthday)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """
        else:
            query = """
                SELECT hr_employee.id 
                FROM hr_employee
                WHERE 
                    EXTRACT(MONTH FROM current_contract_start) * 100 + EXTRACT(DAY FROM current_contract_start)
                    BETWEEN %s * 100 + %s AND %s * 100 + %s
            """

        self.env.cr.execute(query, (from_month, from_day, to_month, to_day))
        employee_ids = [row[0] for row in self.env.cr.fetchall()]
        action = self.sudo().env.ref('hr.open_view_employee_list_my').read()[0]
        action['domain'] = [('id', 'in', employee_ids)]
        return action

