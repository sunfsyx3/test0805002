# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Rent(models.Model):
    _name = 'library.rent'
    _inherit = ['mail.thread', 'mail.message']
    _description = '借书'

    name = fields.Integer(string="借书序号")
    book_ids = fields.Many2many('library.library', ondelete='set null', string="书籍")
    renter_ids = fields.Many2one('library.partner', ondelete='set null', string="借阅者")

    start_date = fields.Datetime(default=fields.Datetime.now, string='借书时间')
    end_date = fields.Datetime(default=fields.Datetime.now, string='还书时间')
    rent_time = fields.Char(compute="compute_rent_time", string='借用时间', store=True)

    state = fields.Selection([('draft', '草稿'), ('rent', '借出'), ('return', '归还')], default='draft', string="状态")

    is_rent = fields.Boolean(string="已借出", track_visibility='onchange')

    out_date = fields.Boolean(default=False, string="已逾期", track_visibility='onchange')

    _sql_constraints = [('uniq_name', 'unique(name)', 'name must be unique !')]

    @api.constrains('start_date', 'end_date')
    def check_date(self):
        for course in self:
            if course.end_date <= course.start_date:
                raise exceptions.ValidationError("结束日期要大于开始日期")

    # @api.constrains('name')
    # def check_name(self):
    #     for course in self:
    #         if len(course.search([('name', '=', course.name)])) > 1:
    #             raise exceptions.ValidationError("已有名称为 \""+course.name+"\" 的记录")

    @api.depends('start_date', 'end_date')
    def compute_rent_time(self):
        for log in self:
            if log.end_date and log.start_date:
                log.rent_time = str(log.end_date - log.start_date)
            else:
                log.rent_time = None

    @api.multi
    def rent_book(self):
        flag = False
        for task in self:
            for book in task.book_ids:
                if book.book_rent or task.is_rent:
                    flag = True
        if flag:
            raise exceptions.ValidationError("已借出")
        else:
            self.is_rent = True
            self.state = 'rent'
            # self.write({'start_date': fields.Datetime.now()})
            # self.write({'end_date': None})
            for book in self.book_ids:
                book.write({'book_rent': True})

    @api.multi
    def return_book(self):
        for task in self:
            if not task.is_rent:
                raise exceptions.ValidationError("已归还")
            else:
                task.is_rent = False
                self.state = 'return'
                task.write({'out_date': False})
                # task.write({'end_date': fields.Datetime.now()})
                for book in self.book_ids:
                    book.write({'book_rent': False})

    @api.multi
    def draft_book(self):
        for task in self:
            if task.is_rent:
                raise exceptions.Warning("提示：已借出，不能设置为草稿")
            else:
                task.is_rent = False
                self.state = 'draft'

    @api.multi
    def submit_amount_plan(self):
        print("++++++++++++++++++++++")
        for plan in self.search([('end_date', '<', fields.Datetime.now())]):
            if plan.is_rent:
                plan.write({'out_date': True})
                print("逾期")
                # plan.message_post("24444444444444444", message_type="notification", subtype='mail.mt_note')
                # plan.portal_chatter_init(self, plan.out_date)
                # return 'library_rent.mt_state_change'
            else:
                plan.write({'out_date': False})

