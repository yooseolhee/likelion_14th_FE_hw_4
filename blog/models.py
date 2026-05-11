"""
blog/models.py

아기 사자 여러분은 이 파일을 수정할 일이 거의 없어요.
어떤 데이터 구조로 정의되어 있는지 참고하면 됩니다.

template에서 접근 방식 예시:
  {{ post.title }}              # 단순 필드
  {{ post.category.label }}     # ForeignKey 관계 (Category 객체 → label 필드)
  {% for tag in post.tags.all %}  # ManyToMany 관계
"""
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Tag(models.Model):
    """포스트 태그 (#design-system, #css 등)"""
    slug = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=50)

    def __str__(self):
        return f'#{self.slug}'


class Category(models.Model):
    """카테고리 (Frontend, TypeScript, AI 등 — Tech 글 분류용)"""
    slug = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'label']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.label


class TechPost(models.Model):
    """기술 블로그 포스트"""
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, help_text='영문 부제')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tech_posts')
    body = models.TextField(blank=True, help_text='Markdown-lite. h2는 ## 로 시작')
    read_minutes = models.PositiveIntegerField(default=5)
    series_label = models.CharField(max_length=80, blank=True, help_text='ex. series 5/8')
    views = models.PositiveIntegerField(default=0)
    license = models.CharField(max_length=50, default='CC BY 4.0')
    published_at = models.DateField()
    edited_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tech_detail', args=[self.slug])

    @property
    def date_display(self):
        """template에서 {{ post.date_display }}로 접근 — '2026.04.28' 형식"""
        return self.published_at.strftime('%Y.%m.%d')

    @property
    def edited_display(self):
        return self.edited_at.strftime('%Y.%m.%d') if self.edited_at else ''

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:200] or 'post'
        super().save(*args, **kwargs)


class Comment(models.Model):
    """포스트 댓글
    - 인증 도입 후: user FK가 source of truth. author_name은 표시 캐시.
    - 기존 익명 댓글은 user=None으로 남아있고 author_name으로만 표시.
    """
    post = models.ForeignKey(TechPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='comments',
    )
    author_name = models.CharField(max_length=40)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author_name}: {self.body[:30]}'

    @property
    def date_display(self):
        return self.created_at.strftime('%Y.%m.%d')

    @property
    def display_name(self):
        if self.user_id:
            return self.user.first_name or self.user.username
        return self.author_name or 'anonymous'

    @property
    def initials(self):
        name = self.display_name
        return name[:2].upper() if name else 'AN'


class DailyCategory(models.Model):
    """일일 노트 카테고리 (커피, 책, 산책 등)"""
    slug = models.SlugField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'label']
        verbose_name_plural = 'Daily categories'

    def __str__(self):
        return self.label


class DailyEntry(models.Model):
    """일일 노트 항목"""
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(DailyCategory, on_delete=models.PROTECT, related_name='entries')
    excerpt = models.TextField()
    published_at = models.DateField()

    class Meta:
        ordering = ['-published_at']
        verbose_name_plural = 'Daily entries'

    def __str__(self):
        return self.title

    @property
    def date_display(self):
        return self.published_at.strftime('%Y.%m.%d')


class Project(models.Model):
    """프로젝트 카드"""
    STATUS_CHOICES = [
        ('live', 'Live'),
        ('wip', 'In progress'),
        ('archive', 'Archived'),
    ]

    slug = models.SlugField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    blurb = models.TextField()
    year = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='live')
    tags = models.CharField(max_length=300, blank=True, help_text='쉼표로 구분')
    external_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', '-year']

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def status_label(self):
        mapping = {'live': 'live', 'wip': 'wip · in progress', 'archive': 'archived'}
        return mapping.get(self.status, self.status)


class Profile(models.Model):
    """About 페이지용 프로필 — 사이트 전역 설정처럼 단일 row"""
    display_name = models.CharField(max_length=80, default='아기사자')
    headline_eyebrow = models.CharField(max_length=80, default='ABOUT')
    headline = models.CharField(max_length=120, default='안녕하세요, 아기사자예요.')
    role_line = models.CharField(max_length=160, default='Frontend engineer · 서울 · she/her')
    bio_ko = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
    avatar_initials = models.CharField(max_length=4, default='BL')

    def __str__(self):
        return self.display_name


class SkillGroup(models.Model):
    """프로필 Skills 섹션의 한 행 (frontend/backend/tools 등)"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skill_groups')
    label = models.CharField(max_length=50)
    skills = models.CharField(max_length=400, help_text='쉼표로 구분')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.label}: {self.skills}'

    @property
    def skill_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class Education(models.Model):
    """프로필 Education 섹션의 한 행"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='education')
    period = models.CharField(max_length=50)
    title = models.CharField(max_length=120)
    subtitle = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Education'

    def __str__(self):
        return f'{self.period} · {self.title}'
