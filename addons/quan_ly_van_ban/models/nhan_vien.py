# -*- coding: utf-8 -*-

from odoo import models, fields, api

class NhanVien(models.Model):
    _inherit = 'nhan_vien'

    van_ban_den_ids = fields.One2many(
        'van_ban_den',
        'nhan_vien_xu_ly_id',
        string='Văn bản phụ trách'
    )
    van_ban_den_count = fields.Integer(
        compute='_compute_vb_count'
    )

    def _compute_vb_count(self):
        for rec in self:
            rec.van_ban_den_count = self.env['van_ban_den'].search_count([
                ('nhan_vien_xu_ly_id', '=', rec.id)
            ])

    def action_open_van_ban_den(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Văn bản đến',
            'res_model': 'van_ban_den',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_xu_ly_id', '=', self.id)],
        }
