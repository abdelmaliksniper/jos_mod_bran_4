#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import base64
import io
from odoo import _, api, fields, models, tools, SUPERUSER_ID
from wand.image import Image as wImage
from wand.drawing import Drawing
from wand.color import Color
from .arabic_reshaper import reshape
from .bidi.algorithm import get_display
#from escpos.printer import *
from odoo.exceptions import UserError, ValidationError
import math


class PosOrder(models.Model):
    _inherit = "pos.order"
    #FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    @api.model
    def pos_malik(self, data):
        try:
            y = 0
            for aa in data['receipt']['orderlines']:
                y = y + 1
            fonts = [os.path.dirname(__file__) + '/img/KacstOffice.ttf', os.path.dirname(__file__) + '/img/amiri-regular.ttf']
            draw = Drawing()

            img = wImage(width=500, height=260 + y * 75 + 260, background=Color('#ffffff'))
            draw.text_alignment = 'center';
            draw.text_antialias = True
            draw.text_encoding = 'utf-8'
            draw.text_kerning = 0.0
            draw.font_resolution = (1000, 1000)
            draw.font = fonts[0]
            draw.font = fonts[1]
            img.resolution = (1000, 1000)
            draw.font_size = 28
            x = 260
            if data['receipt']['company']['name']:
                draw.text(495 / 2, 20, get_display(reshape(u''.join(data['receipt']['company']['name']))));
            if data['receipt']['company']['email']:
                draw.text(495 / 2, 50, get_display(reshape(u''.join(data['receipt']['company']['email']))));
            if data['receipt']['company']['website']:
                draw.text(495 / 2, 80, get_display(reshape(u''.join(data['receipt']['company']['website']))));
            if data['receipt']['company']['phone']:
                draw.text(495 / 2, 110, get_display(reshape(u''.join(data['receipt']['company']['phone']))));
            if data['receipt']['company']['vat']:
                draw.text(495 / 2, 140, get_display(reshape(u''.join(data['receipt']['company']['vat']))) + " : " + get_display(
                    reshape(u''.join(u"الرقم الضريبي"))));

            draw.text_alignment = 'right';
            draw.text(500, 170,
                      "...........................................................................................................")
            draw.text(500, 175,
                      "...........................................................................................................")

            draw.text(495, 200, get_display(reshape(u'الصنـــف')));
            draw.text(160, 200, get_display(reshape(u'الكميـــة')));
            draw.text(60, 200, get_display(reshape(u'السعـــر\n')))
            draw.text(500, 225,
                      "...........................................................................................................")
            draw.text(500, 230,
                      "...........................................................................................................")

            t = 0
            for malik in data['receipt']['orderlines']:
                draw.text(495, x, get_display(reshape(
                    u''.join(malik['product_name']))));
                draw.text(160, x + 30, str(malik['quantity']));
                draw.text(90, x + 30, str(float(malik['price_with_tax'])))
                if malik['discount'] > 0:
                    draw.text(410, x + 30, get_display(reshape(u'خصـم')));
                    draw.text(475, x + 30, str(malik['discount']));
                    draw.text(495, x + 30, '%');
                if malik['tax'] > 0:
                    draw.text(290, x + 30, get_display(reshape(u'ضريبة')));
                    draw.text(350, x + 30, str(malik['tax']));
                t += 1
                if t == y:
                    draw.text(500, x + 50, ".........................................................................................................................")
                    draw.text(500, x + 55, ".........................................................................................................................")
                else:
                    draw.text(500, x + 50, "------------------------------------------------------------------------------------------------------")
                x = x + 75
            draw.text(495, x, get_display(reshape(u' ضرائب:')));
            draw.text(75, x, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(410, x, str(float(data['receipt']['total_tax'])));

            draw.text(247, x, get_display(reshape(u' خصم:')));
            #draw.text(80, x + 40, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(170, x, str(float(data['receipt']['total_discount'])));

            draw.text(495, x + 40, get_display(reshape(u' اجمالي:')));
            draw.text(75, x + 40, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(410, x + 40, str(float(data['receipt']['total_with_tax'])));

            draw.text(247, x + 40, get_display(reshape(u'متبقي:')));
            #draw.text(80, x + 120, get_display(reshape(u''.join(self.env.user.company_id.currency_id.symbol))));
            draw.text(170, x + 40, str(float(data['receipt']['change'])));

            draw.text(500, x + 60, "...........................................................................................................")
            draw.text(500, x + 65, "...........................................................................................................")

            draw.text(495, x + 90, get_display(reshape(u'مقــــدم الخدمــــة :')));
            draw.text(300, x + 90, get_display(
                reshape(u''.join(data['receipt']['cashier']))));
            if data['receipt']['client']:
                draw.text(495, x + 130, get_display(reshape(u'الزبون :')));
                draw.text(300, x + 130, get_display(reshape(u''.join(data['receipt']['client']))));
            draw.text(500, x + 155, "...........................................................................................................")
            draw.text(500, x + 160, "...........................................................................................................")

            draw.text_alignment = 'center';
            draw.text(495 / 2, x + 190, get_display(reshape(u''.join(data['receipt']['name']))));
            draw.text(495 / 2, x + 220, get_display(reshape(u''.join(data['receipt']['date']['localestring']))));
            draw(img)
            return img.make_blob('png').encode('base64')
        except:
            pass
#FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
class PosConfig(models.Model):
    _inherit = 'pos.config'

    arabic_allow = fields.Boolean("Allow Arabic Printing", default=False)