from odoo.addons.account.wizard.account_resequence import ReSequenceWizard

# TODO: Odoo BTL - default_get patch must be resolved in a different way than with a monkey patch, the original
#  functionality must remain for the other companies
def _revert_method(cls, name):
    """Revertir el método original llamado 'name'"""
    method = getattr(cls, name)
    setattr(cls, name, method.origin)


def uninstall_hook(cr, registry):
    _revert_method(ReSequenceWizard, "default_get")
