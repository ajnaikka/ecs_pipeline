import base64
import datetime

import requests

from odoo import api, models, fields, tools
import logging

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    checked_in = fields.Binary(string='Checked In',attachment=True)
    checked_out = fields.Binary(string='Checked Out',attachment=True)
    hoursToday = fields.Char(string="sample")

    @api.onchange('checked_in')
    def print_checked_in_image(self):
        if self.checked_in:
            # Do whatever action you want with the uploaded image.
            # Here, let's print the content of the image.
            print("Checking the image iiiiiiiiiiiiiiiiiiiiiiiiii", self.checked_in)
            print("Checking the image iiiiiiiiiiiiiiiiiiiiiiiiii", type(self.checked_in))