from collections import defaultdict

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    add_check_credit = fields.Boolean("Agregar Crédito de Cheques", company_dependent=True)

    @api.depends_context("company")
    @api.depends("add_check_credit")
    def _credit_debit_get(self):
        super()._credit_debit_get()
        company = self.env.company
        if company.country_code != "AR":
            return

        partners = self.filtered("add_check_credit")
        if not partners:
            return

        checks = self.env["l10n_latam.check"].search(
            [
                ("partner_id", "in", partners.ids),
                ("company_id", "=", company.id),
                (
                    "current_journal_id.inbound_payment_method_line_ids.payment_method_id.code",
                    "=",
                    "in_third_party_checks",
                ),
                ("payment_date", ">", fields.Date.context_today(self)),
            ]
        )
        credit_by_partner = defaultdict(float)
        for check in checks:
            credit_by_partner[check.partner_id.id] += check.currency_id._convert(
                check.amount,
                company.currency_id,
                company,
                check.payment_date,
            )
        for partner in partners:
            partner.credit += credit_by_partner[partner.id]
