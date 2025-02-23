from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property"
    _order = "id desc"

    name = fields.Char(text="Title", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Availability Date", copy=False,
                                    default=fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garage Area")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    # active = fields.Boolean(string="Active", default=False)
    state = fields.Selection(string="State",
                             selection=[('new', 'New'), ('offer_received', 'Offer received'),
                                        ('offer_accepted', 'Offer accepted'), ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')],
                             default='new'
                             )

    property_type_id = fields.Many2one('estate.property.type', string='Estate property type')

    seller_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company.id)
    buyer_id = fields.Many2one('res.partner', string='Buyer person', copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price")



    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', "Expected price must be strictly positive"),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "Selling price must be positive"),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = 0
            prices = record.offer_ids.mapped('price')
            if len(prices):
                record.best_price = max(prices )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_cancel(self):
        if self.state == "sold":
            raise UserError("Sold properties cannot be cancelled!")
        self.state = "cancelled"
        return True

    def action_sell(self):
        if self.state == "offer_accepted":
            self.state = "sold"
        elif self.state == "cancelled":
            raise UserError("Cancelled properties cannot be set as sold!")
        else:
            raise UserError("The property can't be sold!")


    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            # if record.selling_price != 0 and record.selling_price < (record.expected_price * 0.9):
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price")


    # @api.ondelete(at_uninstall=True)
    def unlink(self):
        if self.state not in ['new', 'canceled']:
            raise UserError("You cannot delete an estate property with status 'New' or 'Canceled'.")
        return super().unlink()
