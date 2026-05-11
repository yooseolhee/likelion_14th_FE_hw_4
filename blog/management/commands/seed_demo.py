"""
python manage.py seed_demo

Figma 화면에 박혀있던 더미 데이터를 DB에 채워 넣어요.
아기 사자 배포용 db.sqlite3는 이 명령을 미리 돌려서 시드된 상태로 동봉됩니다.
"""
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import (
    Category, Comment, DailyCategory, DailyEntry, Education,
    Profile, Project, SkillGroup, Tag, TechPost,
)


class Command(BaseCommand):
    help = '데모 데이터 시드'

    def handle(self, *args, **opts):
        self.stdout.write('🌱 시드 시작…')

        # ===== Tech 카테고리 =====
        cat_data = [
            ('frontend', 'Frontend', 1),
            ('typescript', 'TypeScript', 2),
            ('ai', 'AI', 3),
            ('performance', 'Performance', 4),
            ('series-ds', 'Series · DS', 5),
        ]
        cat_map = {}
        for slug, label, order in cat_data:
            obj, _ = Category.objects.update_or_create(
                slug=slug, defaults={'label': label, 'order': order}
            )
            cat_map[slug] = obj

        # ===== Tags =====
        tag_data = [
            'design-system', 'tokens', 'css', 'trpc', 'types', 'dx',
            'layout', 'ai', 'workflow', 'agents', 'react', 'perf',
            'series', '5/8',
        ]
        tag_map = {}
        for label in tag_data:
            slug = label.replace('/', '-').replace(' ', '-')
            obj, _ = Tag.objects.update_or_create(
                slug=slug, defaults={'label': label}
            )
            tag_map[label] = obj

        # ===== Tech 포스트 =====
        post_data = [
            {
                'slug': 'design-system-that-fits-the-hand',
                'title': '손에 익는 디자인 시스템 만들기',
                'subtitle': 'Designing a system that fits the hand',
                'category': 'frontend',
                'tags': ['design-system', 'tokens', 'css'],
                'read_minutes': 8,
                'series_label': 'series 5/8',
                'views': 1284,
                'published_at': date(2026, 4, 28),
                'edited_at': date(2026, 4, 29),
                'body': """디자인 시스템을 처음 만들 때, 저는 컴포넌트부터 시작했어요. 버튼, 카드, 입력 필드. 그러다 알았죠. 토큰이 없는 컴포넌트는 짐이라는 걸요.

## 토큰이란

토큰은 디자인 결정에 이름을 붙이는 일이에요. --accent는 "주황색"이 아니라 "강조되는 무엇"을 의미하죠.

```
:root {
  --accent: #E8794A;       /* terracotta · primary */
  --accent-hover: #C95A2C; /* deeper rust */
  --bg-page: #F5EDE0;      /* page · soft beige */
}
```

이름을 잘 붙이면, 색을 바꾸는 일이 의미를 바꾸는 일이 됩니다. 그게 시스템이에요.

## 단위 결정

스페이싱은 4의 배수, 폰트 사이즈는 모듈러 스케일. 단위에 일관성이 있어야 어디서든 자연스럽게 조립됩니다.

## 빌드 파이프라인

Style Dictionary, Tokens Studio, 또는 자체 CLI. 어느 쪽이든 한 번 빌드하면 CSS, JS, iOS, Android에서 같은 값을 쓰게 만드는 게 핵심이에요.

## 마무리

시스템은 한 번에 완성되지 않아요. 어제 만든 토큰을 오늘 다시 의심하는 일, 그게 시스템을 손에 익히는 과정입니다.""",
                'comments': [
                    ('jaemin', '토큰 네이밍 진짜 어렵죠. semantic 레벨까지 가면 의견 갈리고요.'),
                    ('soyun', '다음 편 기다릴게요. 빌드 파이프라인 부분 궁금해요.'),
                ],
            },
            {
                'slug': 'a-year-with-trpc',
                'title': 'tRPC와 함께한 1년: 좋았던 것, 불편했던 것',
                'subtitle': 'A year with tRPC',
                'category': 'typescript',
                'tags': ['trpc', 'types', 'dx'],
                'read_minutes': 6,
                'published_at': date(2026, 4, 21),
                'body': '풀스택 프로젝트에 tRPC를 도입한 지 1년이 지났어요. 좋았던 점은 단연 타입 추론이고, 어색했던 점은 미들웨어 설계였습니다.\n\n## 좋았던 것\n\n클라이언트가 서버 API의 시그니처를 그대로 알고 있다는 건, 한 번 익숙해지면 다시 돌아가기 어려워요.',
                'comments': [],
            },
            {
                'slug': 'i-came-around-to-container-queries',
                'title': 'CSS Container Queries, 결국 쓰게 되더라',
                'subtitle': 'I came around to container queries',
                'category': 'frontend',
                'tags': ['css', 'layout'],
                'read_minutes': 5,
                'published_at': date(2026, 4, 14),
                'body': '컨테이너 쿼리는 처음엔 과한 도구처럼 보였어요. 카드 컴포넌트가 자기 부모의 크기에 따라 모양을 바꾼다는 게 어색했거든요.\n\n## 그래도 쓰게 된 이유\n\n같은 카드를 사이드바와 메인 영역에서 동시에 쓸 일이 생기니까요.',
                'comments': [],
            },
            {
                'slug': 'beyond-vibe-coding',
                'title': 'Vibe coding 다음 단계 — 워크플로우 만들기',
                'subtitle': 'Beyond vibe coding',
                'category': 'ai',
                'tags': ['ai', 'workflow', 'agents'],
                'read_minutes': 12,
                'published_at': date(2026, 4, 7),
                'body': 'AI에게 "느낌으로" 시키는 단계를 넘어, 단계가 정해진 워크플로우를 짜는 일이 점점 중요해지고 있어요.',
                'comments': [],
            },
            {
                'slug': 'removing-usememo-with-react-19',
                'title': 'React 19 컴파일러로 useMemo를 지웠다',
                'subtitle': 'Removing useMemo with React 19',
                'category': 'performance',
                'tags': ['react', 'perf'],
                'read_minutes': 7,
                'published_at': date(2026, 3, 30),
                'body': 'React 19의 컴파일러가 안정화되면서, 손으로 적던 useMemo의 절반은 사라졌어요.',
                'comments': [],
            },
            {
                'slug': 'five-ways-to-ship-design-tokens',
                'title': '디자인 토큰을 코드로 옮기는 5가지 방법',
                'subtitle': 'Five ways to ship design tokens',
                'category': 'series-ds',
                'tags': ['design-system', 'series', '5/8'],
                'read_minutes': 9,
                'series_label': 'series 5/8',
                'published_at': date(2026, 3, 22),
                'body': 'CSS 변수, JSON, Style Dictionary, Tokens Studio, 그리고 직접 만든 빌더. 각각 장단점이 있어요.',
                'comments': [],
            },
        ]

        for p in post_data:
            tags = p.pop('tags')
            cat_slug = p.pop('category')
            comments = p.pop('comments')
            obj, _ = TechPost.objects.update_or_create(
                slug=p['slug'],
                defaults={**p, 'category': cat_map[cat_slug]},
            )
            obj.tags.set([tag_map[t] for t in tags])
            # 댓글 시드 (기존 댓글 삭제 후 새로)
            obj.comments.all().delete()
            for name, body in comments:
                Comment.objects.create(post=obj, author_name=name, body=body)

        # ===== Daily =====
        dcat_data = [
            ('coffee', '커피', 1), ('book', '책', 2), ('walk', '산책', 3),
            ('music', '음악', 4), ('cooking', '요리', 5), ('memo', '메모', 6),
        ]
        dcat_map = {}
        for slug, label, order in dcat_data:
            obj, _ = DailyCategory.objects.update_or_create(
                slug=slug, defaults={'label': label, 'order': order}
            )
            dcat_map[slug] = obj

        daily_data = [
            ('coffee', date(2026, 4, 30),
             '아침 라떼 · 4월 30일', 'A morning latte · Apr 30',
             '오늘은 새 원두로 내렸어요. 산미가 도드라져서 우유를 조금만 넣었어요.'),
            ('book', date(2026, 4, 27),
             '읽고 있는 책: A Philosophy of Software Design', 'Reading: APoSD',
             '복잡성을 줄이는 일은 결국 인내심의 문제라는 챕터가 좋았어요.'),
            ('walk', date(2026, 4, 25),
             '서울숲 · 토요일 산책', 'Saturday walk',
             '벚꽃이 거의 다 졌고, 새로 핀 잎이 노랗게 올라오는 중이에요.'),
            ('music', date(2026, 4, 22),
             '이번 주 들은 것 · week 17', "This week's rotation",
             'Khruangbin · Mac DeMarco · 그리고 옛날 김창완 노래.'),
            ('cooking', date(2026, 4, 18),
             '주말 김밥, 실패한 버전', 'Weekend kimbap (failed)',
             '밥이 너무 질었지만 그래도 맛있었어요. 다음엔 식초를 줄여볼게요.'),
            ('memo', date(2026, 4, 14),
             '4월의 작은 결심들', 'Tiny April resolutions',
             '작은 것을 끝까지 마치기. 미루기 전에 5분만 시작하기.'),
        ]
        for cat_slug, pub, title, title_en, excerpt in daily_data:
            slug = title.replace(' ', '-').replace('·', '-').replace('/', '-')[:80]
            DailyEntry.objects.update_or_create(
                slug=slug,
                defaults={
                    'category': dcat_map[cat_slug],
                    'published_at': pub,
                    'title': title,
                    'title_en': title_en,
                    'excerpt': excerpt,
                },
            )

        # ===== Projects =====
        project_data = [
            ('note-haeun', 'note.haeun',
             '마크다운 기반 개인 위키 — 로컬 우선, 버전 히스토리 내장',
             '2026', 'live', 'React, Tauri, SQLite', 1),
            ('tokens-css', 'tokens.css',
             'Figma 변수를 CSS 토큰으로 빌드하는 작은 CLI',
             '2026', 'wip', 'Node, TypeScript', 2),
            ('slowread', 'slowread',
             'RSS를 천천히 — 하루 3개 글만 보여주는 리더',
             '2025', 'live', 'Next.js, tRPC', 3),
            ('studio-m-ui-kit', 'studio.m UI Kit',
             '회사에서 운영 중인 사내 디자인 시스템',
             '2025', 'live', 'React, Storybook', 4),
            ('paper-deck', 'paper-deck',
             'HTML 슬라이드를 노트처럼 — 베이지 톤 deck framework',
             '2024', 'archive', 'Vanilla, Web Component', 5),
            ('morning-pages', 'morning-pages',
             '매일 아침 3페이지를 위한 어두운 글쓰기 앱',
             '2024', 'archive', 'SwiftUI, iOS', 6),
        ]
        for slug, name, blurb, year, status, tags, order in project_data:
            Project.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name, 'blurb': blurb, 'year': year,
                    'status': status, 'tags': tags, 'order': order,
                },
            )

        # ===== Profile =====
        profile, _ = Profile.objects.update_or_create(
            id=1,
            defaults={
                'display_name': '아기사자',
                'headline_eyebrow': 'ABOUT',
                'headline': '안녕하세요, 아기사자예요.',
                'role_line': 'Frontend engineer · 서울 · she/her',
                'bio_ko': '작은 도구를 만들고, 그 과정을 글로 남기는 걸 좋아합니다. '
                          '요즘은 디자인 시스템과 타입 안전한 풀스택 구조에 관심이 많아요. '
                          '이 페이지는 제가 매일 조금씩 정리해 두는 노트예요.',
                'bio_en': 'Frontend engineer based in Seoul. I make small tools and write '
                          'about the process. Currently into design systems and type-safe '
                          'full-stack patterns.',
                'avatar_initials': 'BL',
            },
        )

        profile.skill_groups.all().delete()
        skill_data = [
            ('frontend', 'React, TypeScript, Next.js, Vite, Tailwind', 1),
            ('backend', 'Node.js, PostgreSQL, Prisma, tRPC', 2),
            ('tools', 'Figma, Git, Linear, Notion', 3),
        ]
        for label, skills, order in skill_data:
            SkillGroup.objects.create(
                profile=profile, label=label, skills=skills, order=order
            )

        profile.education.all().delete()
        edu_data = [
            ('2020 – 2024', '동국대학교 컴퓨터공학', 'B.S. · GPA 3.9 / 4.3', 1),
            ('2023 (summer)', 'Recurse Center', 'Independent study, NYC', 2),
            ('2019 – 2020', '온라인 코스 · MIT 6.006', 'Algorithms (audit)', 3),
        ]
        for period, title, sub, order in edu_data:
            Education.objects.create(
                profile=profile, period=period, title=title,
                subtitle=sub, order=order,
            )

        # superuser (admin 패널 접근용 — 강사가 데이터 추가/수정할 때 필요)
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='admin', email='admin@example.com', password='admin1234'
            )
            self.stdout.write('  👤 superuser admin/admin1234 생성')

        self.stdout.write(self.style.SUCCESS('✅ 시드 완료!'))
        self.stdout.write('   • TechPost: %d개' % TechPost.objects.count())
        self.stdout.write('   • DailyEntry: %d개' % DailyEntry.objects.count())
        self.stdout.write('   • Project: %d개' % Project.objects.count())
        self.stdout.write('   • Comment: %d개' % Comment.objects.count())
        self.stdout.write('   • admin 계정: admin / admin1234')
