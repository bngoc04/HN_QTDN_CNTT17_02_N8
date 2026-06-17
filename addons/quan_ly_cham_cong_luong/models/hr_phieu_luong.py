# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HRPhieuLuong(models.Model):
    _name = 'hr_phieu_luong'
    _description = 'Phiếu lương tháng nhân viên'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True)
    thang = fields.Integer("Tháng", required=True, default=lambda self: fields.Date.today().month)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    
    so_ngay_di_lam = fields.Float("Số ngày đi làm thực tế", compute="_compute_luong_data", store=True)
    luong_co_ban = fields.Float("Lương cơ bản (VND)", compute="_compute_luong_data", store=True)
    phu_cap = fields.Float("Phụ cấp (VND)", compute="_compute_luong_data", store=True)
    khen_thuong = fields.Float("Khen thưởng (VND)", compute="_compute_luong_data", store=True)
    ky_luat = fields.Float("Kỷ luật (VND)", compute="_compute_luong_data", store=True)
    
    thuc_linh = fields.Float("Thực lĩnh (VND)", compute="_compute_thuc_linh", store=True)

    _sql_constraints = [
        ('nhan_vien_thang_nam_unique', 'unique(nhan_vien_id, thang, nam)', 'Mỗi nhân viên chỉ có một phiếu lương mỗi tháng!')
    ]

    @api.constrains('thang', 'nam')
    def _check_thang_nam(self):
        for record in self:
            if record.thang < 1 or record.thang > 12:
                raise ValidationError("Tháng phải từ 1 đến 12!")
            if record.nam < 2000:
                raise ValidationError("Năm phải từ 2000 trở đi!")

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_luong_data(self):
        for record in self:
            if not record.nhan_vien_id or not record.thang or not record.nam:
                record.so_ngay_di_lam = 0.0
                record.luong_co_ban = 0.0
                record.phu_cap = 0.0
                record.khen_thuong = 0.0
                record.ky_luat = 0.0
                continue
            
            # 1. Get basic salary and allowances
            luong_rec = self.env['hr_luong_co_ban'].search([('nhan_vien_id', '=', record.nhan_vien_id.id)], limit=1)
            record.luong_co_ban = luong_rec.luong_co_ban if luong_rec else 0.0
            record.phu_cap = (luong_rec.phu_cap_an_trua + luong_rec.phu_cap_trach_nhiem) if luong_rec else 0.0

            # 2. Get date range
            try:
                start_date = datetime.date(record.nam, record.thang, 1)
                if record.thang == 12:
                    end_date = datetime.date(record.nam + 1, 1, 1) - datetime.timedelta(days=1)
                else:
                    end_date = datetime.date(record.nam, record.thang + 1, 1) - datetime.timedelta(days=1)
            except ValueError:
                record.so_ngay_di_lam = 0.0
                record.khen_thuong = 0.0
                record.ky_luat = 0.0
                continue

            # 3. Compute working days from attendance
            cham_cong_recs = self.env['hr_cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', start_date),
                ('ngay_cham_cong', '<=', end_date)
            ])
            so_ngay = 0.0
            for cc in cham_cong_recs:
                if cc.trang_thai == 'di_lam':
                    so_ngay += 1.0
                elif cc.trang_thai == 'nua_ngay':
                    so_ngay += 0.5
            record.so_ngay_di_lam = so_ngay

            # 4. Compute reward and discipline
            kkt_recs = self.env['hr_khen_thuong_ky_luat'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_ap_dung', '>=', start_date),
                ('ngay_ap_dung', '<=', end_date)
            ])
            record.khen_thuong = sum(r.so_tien for r in kkt_recs if r.loai_quyet_dinh == 'khen_thuong')
            record.ky_luat = sum(r.so_tien for r in kkt_recs if r.loai_quyet_dinh == 'ky_luat')

    @api.depends('luong_co_ban', 'so_ngay_di_lam', 'phu_cap', 'khen_thuong', 'ky_luat')
    def _compute_thuc_linh(self):
        for record in self:
            record.thuc_linh = (record.luong_co_ban / 26.0) * record.so_ngay_di_lam + record.phu_cap + record.khen_thuong - record.ky_luat

    def action_recompute(self):
        for record in self:
            record._compute_luong_data()
            record._compute_thuc_linh()
