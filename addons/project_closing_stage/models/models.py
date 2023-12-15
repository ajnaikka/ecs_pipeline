# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, SUPERUSER_ID, _

class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    is_closed = fields.Boolean('Closing Stage', help="Tasks in this stage are considered as closed.")

# class Project(models.Model):
#     _inherit = "project.project"
#
#     def _compute_task_count(self):
#         task_data = self.env['project.task'].read_group(
#             [('project_id', 'in', self.ids), '|', '&', ('stage_id.is_closed', '=', False),
#              ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['project_id'], ['project_id'])
#         result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
#         for project in self:
#             project.task_count = result.get(project.id, 0)



class Task(models.Model):
    _inherit = "project.task"

    # is_closed = fields.Boolean(related="stage_id.is_closed", string="Closing Stage", readonly=True, related_sudo=False)


    def _get_default_stage_id(self):
        """ Gives default stage_id """
        project_id = self.env.context.get('default_project_id')
        if not project_id:
            return False
        return self.stage_find(project_id, [('fold', '=', False), ('is_closed', '=', False)])

    @api.depends('project_id')
    def _compute_stage_id(self):
        for task in self:
            if task.project_id:
                if task.project_id not in task.stage_id.project_ids:
                    task.stage_id = task.stage_find(task.project_id.id, [
                        ('fold', '=', False), ('is_closed', '=', False)])
            else:
                task.stage_id = False

    # def update_date_end(self, stage_id):
    #     project_task_type = self.env['project.task.type'].browse(stage_id)
    #     if project_task_type.fold or project_task_type.is_closed:
    #         return {'date_end': fields.Datetime.now()}
    #     return {'date_end': False}

