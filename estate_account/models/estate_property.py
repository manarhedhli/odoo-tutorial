from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    def action_sell(self):
        print(" from inherited ".center(50, "-"))

        self.env['account.move'].check_access_rights('create')
        self.env['account.move'].check_access_rule('create')

        invoice = self.env['account.move'].sudo().create({
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
        self.invoice_id = invoice.id
        return super().action_sell()