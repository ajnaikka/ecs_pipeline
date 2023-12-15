# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCorporate(models.Model):
    _name = 'res.corporate'
    _description = 'Corporate Franchise'

    name = fields.Char(index=True, default_export_compatible=True)
    code = fields.Char('Corporate Code')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    email = fields.Char('Email')
    phone = fields.Char(unaccent=False)
    mobile = fields.Char(unaccent=False)

    user_id = fields.Many2one('res.users', 'Corporate User')
    parent_id = fields.Many2one('res.corporate', string='Corporate', index=True)
    is_franchise = fields.Boolean(string='Is a Franchise', default=False)
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company)

    def create_corporate_user(self):
        user_group = self.env.ref("base.group_user") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'login': record.email,
                    'groups_id': user_group,
                    'tz': self._context.get('tz'),
                })
                sale_own_group = self.env.ref('sales_team.group_sale_salesman')
                sale_own_group.write({'users': [(4, user_id.id)]})
                cc_portal_group = self.env.ref('asbm_corporate.cc_portal_group')
                cc_portal_group.write({'users': [(4, user_id.id)]})
                user_id.partner_id.email = record.email
                user_id.action_reset_password()
                record.user_id = user_id.id

