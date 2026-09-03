from odoo import models


class AccountAccount(models.Model):
    _inherit = "account.account"

    def write(self, vals):
        res = super().write(vals)
        accounts = self.filtered(lambda account: account.company_id.country_code == "AR")
        if "reconcile" in vals and accounts:
            checks = self.env["l10n_latam.check"].search(
                [
                    ("outstanding_line_id.account_id", "in", accounts.ids),
                ]
            )
            checks._compute_issue_state()
        return res
