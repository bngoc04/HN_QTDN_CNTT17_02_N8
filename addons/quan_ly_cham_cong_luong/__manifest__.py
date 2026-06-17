# -*- coding: utf-8 -*-
{
    'name': 'Quản lý Chấm công & Tính lương',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Module chấm công và tính lương nhân viên',
    'description': """
        Module hỗ trợ chấm công hằng ngày, quản lý lương cơ bản, phụ cấp,
        ghi nhận khen thưởng kỷ luật và tự động tính toán phiếu lương tháng cho nhân viên.
    """,
    'author': 'Antigravity',
    'depends': ['base', 'nhan_su'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_luong_co_ban_views.xml',
        'views/hr_cham_cong_views.xml',
        'views/hr_khen_thuong_ky_luat_views.xml',
        'views/hr_phieu_luong_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
}
