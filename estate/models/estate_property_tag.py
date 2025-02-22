from odoo import api, models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the estate property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]