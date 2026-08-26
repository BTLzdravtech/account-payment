from psycopg2.extras import Json


def migrate(cr, version):
    """Convert add_check_credit to the JSONB format used by company-dependent fields."""
    if not version:
        return

    cr.execute(
        """
        SELECT udt_name
          FROM information_schema.columns
         WHERE table_name = 'res_partner'
           AND column_name = 'add_check_credit'
        """
    )
    column = cr.fetchone()
    if not column or column[0] == "jsonb":
        return

    cr.execute(
        """
        SELECT COALESCE(jsonb_object_agg(company.id::text, TRUE), '{}'::jsonb)
          FROM res_company AS company
          JOIN res_partner AS partner ON partner.id = company.partner_id
     LEFT JOIN res_country AS fiscal_country ON fiscal_country.id = company.account_fiscal_country_id
     LEFT JOIN res_country AS partner_country ON partner_country.id = partner.country_id
         WHERE fiscal_country.code = 'AR' OR partner_country.code = 'AR'
        """
    )
    ar_company_values = cr.fetchone()[0]
    cr.execute(
        """
        ALTER TABLE res_partner
        ALTER COLUMN add_check_credit DROP DEFAULT,
        ALTER COLUMN add_check_credit TYPE jsonb
        USING CASE
            WHEN add_check_credit THEN %s::jsonb
            ELSE NULL
        END
        """,
        [Json(ar_company_values)],
    )
