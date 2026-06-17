# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HRChamCong(models.Model):
    _name = 'hr_cham_cong'
    _description = 'Bảng dữ liệu chấm công hằng ngày'
    _order = 'ngay_cham_cong desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    ngay_cham_cong = fields.Date("Ngày chấm công", required=True, default=fields.Date.context_today)
    trang_thai = fields.Selection([
        ('di_lam', 'Đi làm đủ ngày'),
        ('nua_ngay', 'Làm nửa ngày'),
        ('nghi_co_phep', 'Nghỉ có phép'),
        ('nghi_khong_phep', 'Nghỉ không phép')
    ], string="Trạng thái công", default='di_lam', required=True)
    so_gio_tang_ca = fields.Float("Số giờ tăng ca (OT)", default=0.0)
    nguoi_xac_nhan = fields.Char("Người kiểm tra xách nhận")

    _sql_constraints = [
        ('nhan_vien_ngay_unique', 'unique(nhan_vien_id, ngay_cham_cong)', 'Mỗi nhân viên chỉ được chấm công một lần mỗi ngày!')
    ]
