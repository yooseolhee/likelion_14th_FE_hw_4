# 개인 기술 블로그 클론 코딩

## 🚀 실행 방법

처음 클론한 경우 `db.sqlite3`가 없으므로 아래 순서대로 진행하세요.

```bash
# 1. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate     # Windows: source venv/Scripts/activate

# 2. Django 설치
pip install 'django>=5.0,<6.0'

# 3. DB 생성 + 테이블 스키마 적용
python manage.py migrate

# 4. 데모 데이터 시딩 (TechPost, Project, Profile 등 샘플 데이터 삽입)
python manage.py seed_demo

# 5. admin 계정 생성 — /admin/ 접속용
python manage.py createsuperuser

# 6. 개발 서버 실행
python manage.py runserver
```

브라우저에서 `http://localhost:8000/` 접속.

> **데이터를 초기화하려면**: `rm db.sqlite3 && python manage.py migrate && python manage.py seed_demo`

---

## 🔄 View ↔ Template 데이터 흐름

`blog/views.py`가 template에 넘기는 데이터 + JSON API 스펙. 프론트엔드 구현에 필요한 부분만 정리.

### 모든 페이지 자동 주입

`blog/context_processors.py:site_meta` + Django auth middleware에서 모든 template에 자동으로 들어옵니다.

| 변수                                                           | 타입                             | 용도                                  |
| -------------------------------------------------------------- | -------------------------------- | ------------------------------------- |
| `BRAND_NAME`, `BRAND_INITIALS`, `BRAND_EYEBROW`, `FOOTER_LEFT` | str                              | 헤더·푸터 텍스트                      |
| `NAV_ITEMS`                                                    | list[dict: key, label, url_name] | 네비 메뉴 렌더링                      |
| `user`                                                         | User \| AnonymousUser            | `{% if user.is_authenticated %}` 분기 |

### 페이지별 context

| URL             | template             | 주요 변수                                                                                                                  |
| --------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `/`             | `home.html`          | `hero` (dict), `areas` (list[dict]), `featured` (TechPost), `others` (list[TechPost]), `latest_dailies` (list[DailyEntry]) |
| `/tech/`        | `tech_list.html`     | `posts` (list[TechPost]), `categories` (list[Category])                                                                    |
| `/tech/<slug>/` | `tech_detail.html`   | `post` (TechPost), `sections` (list[dict: kind, text, anchor])                                                             |
| `/about/`       | `profile.html`       | `profile` (Profile)                                                                                                        |
| `/projects/`    | `projects_list.html` | `projects` (list[Project]), `selected_status` (str)                                                                        |
| `/daily/`       | `daily_list.html`    | `entries` (list[DailyEntry]), `categories` (list[DailyCategory])                                                           |
| `/login/`       | `login.html`         | `error` (str), `username` (str, 입력값 유지), `next_url` (str)                                                             |
| `/signup/`      | `signup.html`        | `errors` (list[str]), `name` (str), `username` (str)                                                                       |

### JSON API: `/api/posts/<slug>/comments/`

| 메서드 | 인증                    | 요청 body     | 응답                                      |
| ------ | ----------------------- | ------------- | ----------------------------------------- |
| GET    | 불필요                  | —             | `{comments: [{name, body, date}], count}` |
| POST   | **필수** (비로그인 401) | `{body: str}` | `{comment: {name, body, date}, count}`    |

> POST 시 작성자는 `request.user`로 자동 결정 (클라이언트가 name 안 보냄).

### 객체별 자주 쓰는 속성

template에서 위 변수들에 접근할 때 쓰는 필드/property:

| 객체                             | 속성                                                                                                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **TechPost**                     | `title`, `subtitle`, `slug`, `body`, `category.label`, `tags.all`, `date_display`, `edited_display`, `read_minutes`, `series_label`, `license`, `views` |
| **Comment**                      | `display_name`, `body`, `date_display`, `initials` (모두 property — 로그인/익명 자동 분기)                                                              |
| **Category** / **DailyCategory** | `slug`, `label` (필터 칩)                                                                                                                               |
| **Project**                      | `name`, `blurb`, `year`, `status_label`, `tag_list`, `external_url`                                                                                     |
| **Profile**                      | `display_name`, `headline`, `role_line`, `bio_ko`, `bio_en`, `skill_groups.all`, `education.all`                                                        |
| **DailyEntry**                   | `title`, `excerpt`, `category.label`, `date_display`                                                                                                    |

---

## 🛠️ Admin 패널

`/admin/` 경로로 접속, `admin / admin1234`로 로그인.

수정 가능한 것:

- TechPost (제목, 본문, 카테고리, 태그 등)
- Comment (검토/삭제)
- DailyEntry, Project
- Profile + SkillGroup + Education (inline 편집)
