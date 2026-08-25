import logging

from odoo import SUPERUSER_ID, api


_logger = logging.getLogger(__name__)

REPAIR_DATE_FROM = "2026-02-10"
REPAIR_DATE_TO = "2026-02-28"


def migrate(cr, version):
    """Backfill the outstanding line of own checks affected during the repair window."""
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    for company in env["res.company"].search([]):
        checks = env["l10n_latam.check"].with_company(company).search(
            [
                ("payment_id.company_id", "=", company.id),
                ("payment_method_line_id.code", "=", "own_checks"),
                ("payment_id.state", "not in", ["draft", "canceled"]),
                ("outstanding_line_id", "=", False),
                ("create_date", ">=", REPAIR_DATE_FROM),
                ("create_date", "<", REPAIR_DATE_TO),
            ]
        )
        for check in checks:
            payment_method_lines = check.payment_id.journal_id.outbound_payment_method_line_ids.filtered(
                lambda line: line.name == check.payment_method_line_id.name
                and line.payment_method_id == check.payment_method_line_id.payment_method_id
            )
            accounts = payment_method_lines.payment_account_id
            if len(accounts) != 1:
                _logger.warning(
                    "Skipping check %s: found %s matching outstanding accounts",
                    check.id,
                    len(accounts),
                )
                continue

            lines = check.payment_id.move_id.line_ids.filtered(lambda line: line.account_id == accounts)
            if len(lines) != 1:
                _logger.warning(
                    "Skipping check %s: found %s matching outstanding lines",
                    check.id,
                    len(lines),
                )
                continue
            check.outstanding_line_id = lines
