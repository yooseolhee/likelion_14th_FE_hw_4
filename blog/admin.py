from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug')
    prepopulated_fields = {'slug': ('label',)}


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'order')
    prepopulated_fields = {'slug': ('label',)}


@admin.register(models.TechPost)
class TechPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at', 'views')
    list_filter = ('category', 'published_at')
    search_fields = ('title', 'subtitle', 'body')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    date_hierarchy = 'published_at'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author_name', 'created_at')
    list_filter = ('post',)
    search_fields = ('body',)


@admin.register(models.DailyCategory)
class DailyCategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'order')
    prepopulated_fields = {'slug': ('label',)}


@admin.register(models.DailyEntry)
class DailyEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_at')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'status', 'order')
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('name',)}


class SkillGroupInline(admin.TabularInline):
    model = models.SkillGroup
    extra = 0


class EducationInline(admin.TabularInline):
    model = models.Education
    extra = 0


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'role_line')
    inlines = [SkillGroupInline, EducationInline]
