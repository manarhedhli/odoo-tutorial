from odoo import api, models, fields
from datetime import timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer concerning the estate property"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one('res.partner', string="Partner")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date(
        'Deadline',
        default=lambda self: fields.Date.today() + timedelta(days=7),
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related= "property_id.property_type_id",
        store=True,
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)', "Offer price must be positive"),
    ]

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            elif record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_refuse(self):
        self.status = 'refused'
        return True

    def action_accept(self):
        if self.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError("There is already an accepted offer for this property. Only one offer can be accepted.")
        else:
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.status = 'accepted'
            self.property_id.state = "offer_accepted"
            for offer in self.property_id.offer_ids:
                if offer != self and offer.status != 'refused':
                    offer.status = 'refused'
        return True

    @api.model
    def create(self, vals):
        prop = self.env['estate.property'].browse(vals['property_id'])
        prop.state = "offer_received"
        offer_prices = prop.offer_ids.mapped('price')
        if offer_prices:
            max_offer_price = max(offer_prices)
            if vals['price'] < max_offer_price:
                raise UserError("The new offer price must be higher than the maximum price of existing offers.")
        return super().create(vals)




