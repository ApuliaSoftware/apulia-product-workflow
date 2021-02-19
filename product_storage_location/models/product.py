# -*- coding: utf-8 -*-
# Copyright 2021 Ciro Urselli <c.urselli@apuliasoftware.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ProductTemplate(models.Model):

    _inherit = "product.template"

    loc_rack = fields.Char(size=16, compute='_compute_loc',
                           inverse='_set_loc_rack', search='_search_rack')
    loc_row = fields.Char(size=16, compute='_compute_loc',
                          inverse='_set_loc_row', search='_search_row')
    loc_case = fields.Char(size=16, compute='_compute_loc',
                           inverse='_set_loc_case', search='_search_case')

    @api.depends('product_variant_ids', 'product_variant_ids.loc_rack',
                 'product_variant_ids.loc_row', 'product_variant_ids.loc_case')
    def _compute_loc(self):
        unique_variants = self.filtered(
            lambda template: len(template.product_variant_ids) == 1)

        for template in unique_variants:
            template.loc_rack = template.product_variant_ids.loc_rack
            template.loc_row = template.product_variant_ids.loc_row
            template.loc_case = template.product_variant_ids.loc_case

        for template in (self - unique_variants):
            template.loc_rack = ""
            template.loc_row = ""
            template.loc_case = ""

    def _set_loc_rack(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.loc_rack = self.loc_rack

    def _set_loc_row(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.loc_row = self.loc_row

    def _set_loc_case(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.loc_case = self.loc_case

    def _search_rack(self, operator, value):
        products = self.env['product.product'].search(
            [('loc_rack', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]

    def _search_row(self, operator, value):
        products = self.env['product.product'].search(
            [('loc_row', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]

    def _search_case(self, operator, value):
        products = self.env['product.product'].search(
            [('loc_case', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]


class ProductProduct(models.Model):

    _inherit = "product.product"

    loc_rack = fields.Char(size=16)
    loc_row = fields.Char(size=16)
    loc_case = fields.Char(size=16)
