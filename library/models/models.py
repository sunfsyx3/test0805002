# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Library(models.Model):
    _name = 'library.library'
    _description = '图书馆'

    name = fields.Char(string="书名")
    authors = fields.Many2many('library.partner', ondelete='set null', string="作者")
    editors = fields.Many2one('library.partner', ondelete='set null', string="编辑")
    year = fields.Char(string='年份')
    edition = fields.Char(string="版本")
    ISBN = fields.Char(string="ISBN", size=10)

    description = fields.Text(string="书籍描述")
    rent_ids = fields.Many2many('library.rent', string="借书记录")
    book_rent = fields.Boolean(string="已借出")

    _sql_constraints = [('uniq_name', 'unique(name)', 'name must be unique !')]

