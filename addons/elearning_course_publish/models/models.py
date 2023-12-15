# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class Channel(models.Model):
    _inherit = 'slide.channel'

    def action_publish_or_unpublish(self):
        for record in self:
            if self.env.user.has_group('course_frame.group_academy_director'):
                if record.is_published is True:
                    record.is_published = False
                else:
                    record.is_published = True
            else:
                raise AccessError(_("You don't have the access rights to publish/unpublish course."))
