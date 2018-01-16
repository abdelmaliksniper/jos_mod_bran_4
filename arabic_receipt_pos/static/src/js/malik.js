odoo.define('arabic_receipt_pos.posreceipt', function(require){
"use strict";
    var screens = require('point_of_sale.screens');
    var Model = require('web.Model');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
    var QWeb = core.qweb;


    screens.ReceiptScreenWidget.include({

    print_xml: function() {
        var self = this;
        var ord = this.pos.get_order();
        if(self.pos.config.arabic_allow)
        {

        var dataa = {
            receipt: ord.export_for_printing(),
        };
        new Model('pos.order').call('pos_malik', [dataa]).then(function(result){
            //if(result.sig === false){
            var env = {
            malik: result,
            receipt: ord.export_for_printing(),
            };
            var receipt = QWeb.render('Xml_Arabic',env);

            self.pos.proxy.print_receipt(receipt);
            ord._printed = true;
            //}
        });

        }
        else{
            this._super();
        }
    },


    });

});