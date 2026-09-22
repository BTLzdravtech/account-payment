from odoo import models


class AccountAccount(models.Model):
    _inherit = "account.account"

    def write(self, vals):
        res = super().write(vals)
        accounts = self.filtered(
            lambda account: account.company_ids
            and all(company.country_code == "AR" for company in account.company_ids)
        )
        if "reconcile" in vals and accounts:
            checks = self.env["l10n_latam.check"].search(
                [
                    ("outstanding_line_id.account_id", "in", accounts.ids),
                ]
            )
            checks._compute_issue_state()
        return res
