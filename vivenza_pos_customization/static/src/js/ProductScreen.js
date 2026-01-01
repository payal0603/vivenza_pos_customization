odoo.define('vivenza_pos_customization.productScreen', function(require) {
    "use strict";

    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');

    const BiProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            setup() {
                super.setup();
            }

            async _clickProduct(event) {
                const product = event.detail;
                let pos_config = this.env.pos.config;
                
                // Check stock before adding to cart
                if (pos_config.restrict_zero_qty && product.type === 'product') {
                    let available_qty = product.location_qty_available || 0;
                    let order = this.env.pos.get_order();
                    let existing_line = order.get_orderline(product);
                    let current_qty = existing_line ? existing_line.quantity : 0;
                    
                    // Check if adding this product would exceed available stock
                    if (available_qty <= 0) {
                        return this.showPopup('ErrorPopup', {
                            title: this.env._t('Out of Stock'),
                            body: this.env._t(product.display_name + ' is out of stock in this location.'),
                        });
                    }
                    
                    if (current_qty + 1 > available_qty) {
                        return this.showPopup('ErrorPopup', {
                            title: this.env._t('Insufficient Stock'),
                            body: this.env._t(
                                product.display_name + 
                                ' has only ' + available_qty + 
                                ' unit(s) available in this location.'
                            ),
                        });
                    }
                }
                
                // Call parent method to add product
                return super._clickProduct(event);
            }

            async _setValue(val) {
                // Override to check stock when quantity is manually changed
                let pos_config = this.env.pos.config;
                
                if (pos_config.restrict_zero_qty) {
                    let order = this.env.pos.get_order();
                    let selected_line = order.get_selected_orderline();
                    
                    if (selected_line && selected_line.product.type === 'product') {
                        let product = selected_line.product;
                        let available_qty = product.location_qty_available || 0;
                        let new_qty = parseFloat(val);
                        
                        if (new_qty > available_qty) {
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Insufficient Stock'),
                                body: this.env._t(
                                    product.display_name + 
                                    ' has only ' + available_qty + 
                                    ' unit(s) available in this location.'
                                ),
                            });
                            return;
                        }
                    }
                }
                
                return super._setValue(val);
            }

            async _onClickPay() {
                let self = this;
                let order = this.env.pos.get_order();
                let lines = order.get_orderlines();
                let pos_config = self.env.pos.config;
                let call_super = true;

                // Final validation before payment
                if (pos_config.restrict_zero_qty) {
                    for (let line of lines) {
                        let prd = line.product;
                        
                        if (prd.type === 'product') {
                            let available_qty = prd.location_qty_available || 0;
                            
                            if (line.quantity > available_qty) {
                                call_super = false;
                                await self.showPopup('ErrorPopup', {
                                    title: self.env._t('Insufficient Stock'),
                                    body: self.env._t(
                                        prd.display_name + 
                                        ' has only ' + available_qty + 
                                        ' unit(s) available. You are trying to sell ' + 
                                        line.quantity + ' unit(s).'
                                    ),
                                });
                                break;
                            }
                        }
                    }
                }

                if (call_super) {
                    super._onClickPay();
                }
            }
        };

    Registries.Component.extend(ProductScreen, BiProductScreen);

    return ProductScreen;

});