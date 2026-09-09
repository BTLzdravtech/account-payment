from . import models
from . import wizard


def _generate_receiptbooks(env):
    """Create receiptbooks on existing Argentine Payment Pro companies."""
    companies = (
        env["res.company"].search([("chart_template", "!=", False)]).filtered(lambda company: company.use_receiptbook)
    )
    for company in companies:
        env["account.chart.template"]._create_receiptbooks(company)
