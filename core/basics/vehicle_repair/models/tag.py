# -*- coding: utf-8 -*-

from odoo import fields, models


class Tag(models.Model):
    _name = "tag"
    _description = "Vehicle Repair Tags"

    name = fields.Char()
    color = fields.Integer("Color")
