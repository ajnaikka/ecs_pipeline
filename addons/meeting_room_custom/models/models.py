# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class CustomRoomBooking(models.Model):
    _inherit = "room.booking"

    @api.constrains("start_datetime")
    def _check_start_datetime(self):
        for booking in self:
            current_datetime = datetime.now()
            if booking.start_datetime <= current_datetime:
                raise ValidationError(_("Start datetime should be greater than current datetime.Please book the meeting with a 1 hour gap ."))

            min_start_datetime = current_datetime + timedelta(hours=1)
            if booking.start_datetime < min_start_datetime:
                raise ValidationError(_("Start datetime should be at least 1 hour from the current datetime."))

