from . import models
from . import wizard

def _generate_receiptbooks(env):
    """Create receiptbooks on existing companies with chart installed"""
    with_chart_companies = env["res.company"].search([("chart_template", "!=", False)])
    # DONETODO: Odoo BTL - needs to be locked on AR company
    if env.company.country_code == 'AR':
        for company in with_chart_companies:
            env["account.chart.template"]._create_receiptbooks(company)
