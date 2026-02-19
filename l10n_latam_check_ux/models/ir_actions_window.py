# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, http
from odoo.exceptions import ValidationError
from odoo.addons.web.controllers.home import Home
from odoo.http import request, route

# hide_menu_xml_id = "l10n_latam_check_ux.menu_account_check_to_date_report"
block_action_xml_id = "l10n_latam_check_ux.action_account_check_to_date_report"


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    def read(self, fields=None, load='_classic_read'):
        env = self.env
        if env.company.country_code != 'AR':
            block_action = env.ref(block_action_xml_id).id
            if len(self) == 1 and block_action == self.id:
                raise ValidationError(
                    "The view is only visible or AR companies."
                )
        return super().read(fields=fields, load=load)
