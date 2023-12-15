# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class AccessToken(models.TransientModel):
    _name = 'access.token'
    _description = 'Access Token'

    name = fields.Char(string="Access Token",required=True)

    def validate_token(self,token):
        ICP = self.env['ir.config_parameter']
        validity = ICP.sudo().get_param('openeducat_custom.access_token_validity')
        today = fields.Datetime.now()
        timedelta = today - token.create_date
        if timedelta >datetime.timedelta(minutes=int(validity)):
            return False
        return True
    # @api.autovacuum
    # def _clear_access_token(self,*args, **kwargs):
    #     print('inside clear_access_token')
    #     ICP = self.env['ir.config_parameter']
    #     validity = ICP.get_param('openeducat_custom.access_token_validity')
    #     today = fields.Datetime.now()
    #     print('today',today)
    #     token_ids = self.search([])
    #     for token in token_ids:
    #         timedelta = today - token.create_date
    #         print('timedelta',timedelta)
    #         if timedelta >datetime.timedelta(minutes=validity):
    #             token.unlink()
    _sql_constraints = [
        ('unique_token',
         'unique(name)', 'Access token must be unique')]
