from . import models
from . import wizard

def _generate_receiptbooks(env):
    """Create receiptbooks on existing companies with chart installed"""
    with_chart_companies = env["res.company"].search([("chart_template", "!=", False)])
    # filter only AR companies:
    with_chart_companies = with_chart_companies.filtered(lambda c: c.country_code == 'AR')
    # DONETODO: Odoo BTL - needs to be locked on AR company
    for company in with_chart_companies:
        env["account.chart.template"]._create_receiptbooks(company)
