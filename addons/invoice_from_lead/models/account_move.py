from odoo import models, fields, api


class Account(models.Model):
    _inherit = "account.move"

    lead_id= fields.Many2one('crm.lead',string='Lead Id')



