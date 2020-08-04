# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Partner(models.Model):
    _name = 'library.partner'
    _description = '人员'

    name = fields.Char(string="人员")
    is_who = fields.Selection([(1, '作者'), (2, '编辑'), (3, '借阅者'), (4, '图书馆人员')], string="人员种类")

    address = fields.Char(string="地址")
    email = fields.Char(string="电子邮件")
    record_ids = fields.One2many('library.rent', 'renter_ids', ondelete='set null', string="借书记录")
    write_ids = fields.Many2many('library.library', ondelete='set null', string="写书记录")

    _sql_constraints = [('uniq_name', 'unique(name)', 'name must be unique !')]

    @api.model
    def re_action(self):
        return dict(
            name='新建',
            type='ir.actions.act_window',
            res_model='library.partner',
            view_type='form',
            view_mode='form',
            target='new',
        )

    @api.multi
    def great_person(self):
        self.re_action()
        self.write({'name': "测试", 'is_who': 1})
        print("创建")
        # raise exceptions.ValidationError("创建")
        # mass_action = dict(
        #     name='新建',
        #     type='ir.actions.act_window',
        #     res_model='library.partner',
        #     view_type='form',
        #     view_mode='form',
        #     target='new',
        # )
        #
        # return mass_action

    @api.multi
    def modify_person(self):
        for every in self.search([('is_who', '=', '1')]):
            if every.address == "作者地址":
                every.write({'address': "0"})
            else:
                every.write({'address': "作者地址"})
        self.write({'name': "测试modify"})
        print("修改")
        # raise exceptions.ValidationError("修改")

    @api.multi
    def search_person(self):
        for partner in self.search([('is_who', '=', '1')]):
            print(partner.name)
        # raise exceptions.ValidationError("查询")
        return dict(
            name='查询',
            type='ir.actions.act_window',
            res_model='library.partner',
            view_type='form',
            view_mode='tree',
            domain=[('id', 'in', self.search([('is_who', '=', '1')]).ids)],
            target='new',
        )
