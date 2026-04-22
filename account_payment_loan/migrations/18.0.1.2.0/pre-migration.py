import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    _logger.info("START add is_loan_payment to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "is_loan_payment", "boolean"),
    ])
    _logger.info("END add is_loan_payment to account_payment")


    _logger.info("START add loan_surcharge to account_payment")
    openupgrade.add_columns(env, [
        ("account_payment", "loan_surcharge", "float"),
    ])
    _logger.info("END add loan_surcharge to account_payment")