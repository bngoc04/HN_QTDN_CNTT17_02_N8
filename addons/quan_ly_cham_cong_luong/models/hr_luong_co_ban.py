# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HRLuongCoBan(models.Model):
    _name = 'hr_luong_co_ban'
    _description = 'Cấu hình lương cơ bản nhân viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ma_dinh_danh = fields.Char("Mã định danh", related='nhan_vien_id.ma_dinh_danh', store=True)
    luong_co_ban = fields.Float("Lương cơ bản (VND)", required=True, default=0.0)
    phu_cap_an_trua = fields.Float("Phụ cấp ăn trưa", default=0.0)
    phu_cap_trach_nhiem = fields.Float("Phụ cấp trách nhiệm", default=0.0)
    ghi_chu = fields.Text("Ghi chú bổ sung")

    _sql_constraints = [
        ('nhan_vien_unique', 'unique(nhan_vien_id)', 'Mỗi nhân viên chỉ có một cấu hình lương cơ bản!')
    ]
