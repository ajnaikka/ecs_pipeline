from odoo import models, fields, api
import logging
class TravelPlace(models.Model):
    _name = 'travel.place'
    _description = 'Travel Place'

    place_id = fields.Many2one('travel.request', string='Travel Request')
    place = fields.Char(string='Place')
    description = fields.Text(string='Description')
