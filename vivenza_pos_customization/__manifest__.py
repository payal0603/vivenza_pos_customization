{
    "name": "Vivenza POS Customization",
    "summary": "Vivenza POS Customization",
    "version": "16.0.1.0.0",
    "author": "Payal Makvana",
    "license": "LGPL-3",
    "depends": ["point_of_sale"],
    "category": "Point of Sale",
    "description": """
        This module customizes POS functionalities for Vivenza such as:
            1. Restrict selling out-of-stock products based on POS shop location
            2. Cashier selection during session opening and order processing will done through employee badge scan
    """,
    "data": [
        "views/res_config_settings_view.xml",
        "views/pos_config_view.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "/vivenza_pos_customization/static/src/js/ProductScreen.js",
        ]
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "Other proprietary",
}
