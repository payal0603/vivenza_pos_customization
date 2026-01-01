from odoo import models, fields


class PosSession(models.Model):

    # ------------------------------------------------------------------
    # 1. PRIVATE ATTRIBUTES
    # ------------------------------------------------------------------

    _inherit = "pos.session"

    # ------------------------------------------------------------------
    # 2. DEFAULT METHODS AND default_get
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 3. FIELD DECLARATIONS
    # ------------------------------------------------------------------

    restrict_zero_qty = fields.Boolean(string="Restrict Zero Quantity")

    # ------------------------------------------------------------------
    # 4. COMPUTE, INVERSE AND SEARCH METHODS
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 5. SELECTION METHODS
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 6. CONSTRAINS METHODS AND ONCHANGE METHODS
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 7. CRUD METHODS
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 8. ACTION METHODS
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # 9. BUSINESS METHODS
    # ------------------------------------------------------------------

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result["search_params"]["fields"].extend(["qty_available", "type"])
        return result

    def _get_pos_ui_product_product(self, params):
        """Override to add location-based stock quantities"""
        products = super()._get_pos_ui_product_product(params)

        # Get the source location from picking type
        if (
            self.config_id.picking_type_id
            and self.config_id.picking_type_id.default_location_src_id
        ):
            location_id = self.config_id.picking_type_id.default_location_src_id.id

            # Get stock quantities for all products at the specific location
            product_ids = [p["id"] for p in products]
            quants = self.env["stock.quant"].search(
                [("product_id", "in", product_ids), ("location_id", "=", location_id)]
            )

            # Create a dictionary of product_id: available_quantity
            location_stock = {}
            for quant in quants:
                if quant.product_id.id in location_stock:
                    location_stock[quant.product_id.id] += (
                        quant.quantity - quant.reserved_quantity
                    )
                else:
                    location_stock[quant.product_id.id] = (
                        quant.quantity - quant.reserved_quantity
                    )

            # Add location-based quantity to each product
            for product in products:
                product["location_qty_available"] = location_stock.get(
                    product["id"], 0.0
                )

        return products
