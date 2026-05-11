"""
blog/context_processors.py

모든 template에서 사용 가능한 공통 데이터를 만들어요.
NavBar의 메뉴 항목, 브랜드 이름 등.
"""

NAV_ITEMS = [
    {'key': 'home',  'label': 'Home',  'url_name': 'home'},
    {'key': 'about', 'label': 'About', 'url_name': 'profile'},
    {'key': 'tech',     'label': 'Tech',     'url_name': 'tech_list'},
    {'key': 'projects', 'label': 'Projects', 'url_name': 'projects_list'},
    {'key': 'daily', 'label': 'Daily', 'url_name': 'daily_list'},
]


def site_meta(request):
    return {
        'BRAND_NAME': '아기사자의 노트',
        'BRAND_INITIALS': 'BL',
        'BRAND_EYEBROW': '· est. 2026',
        'NAV_ITEMS': NAV_ITEMS,
        'FOOTER_LEFT': '© 2026 아기사자 · made with ☕ & pretendard',
    }
