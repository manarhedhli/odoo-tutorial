from odoo import models, fields


class InheritedUsers(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many("estate.property",
                                   "seller_id",
                                   string="Properties",
                                   domain=[('state', 'in', ['new', 'offer_received'])]
                                   )
