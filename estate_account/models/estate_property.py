from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sell(self):
        print(" from inherited ".center(50, "-"))
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            "invoice_line_ids": [
                (0, 0, {
                    'name': '6% of Selling Price',
                    'quantity': 1,
                    'price_unit': self.selling_price * 0.06,
                }),
                (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        })
        invoice.action_post()
        return super().action_sell()