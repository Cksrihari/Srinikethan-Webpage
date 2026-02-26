from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import SiteSettings, Service, Program, BlogPost, Contact, Testimonial, Workshop

# Custom admin site configuration
admin.site.site_header = "Srinikethan Admin"
admin.site.site_title = "Financial Coach Admin"
admin.site.index_title = "Welcome to Financial Coach Administration"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_title', 'hero_title', 'hero_subtitle', 'about_title', 'about_content')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'twitter_url', 'facebook_url')
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']
    ordering = ['order', 'title']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'price', 'is_featured', 'is_active', 'order']
    list_filter = ['is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'duration', 'price')
        }),
        ('Settings', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'is_featured', 'created_at', 'published_at']
    list_filter = ['is_published', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'tags']
    list_editable = ['is_published', 'is_featured']
    readonly_fields = ['published_at']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_at', 'author')
        }),
        ('SEO', {
            'fields': ('tags', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'inquiry_type', 'subject', 'is_read', 'is_responded', 'created_at']
    list_filter = ['inquiry_type', 'is_read', 'is_responded', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'subject', 'message']
    list_editable = ['is_read', 'is_responded']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'company')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_responded', 'notes', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_responded']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected contacts as read"
    
    def mark_as_responded(self, request, queryset):
        queryset.update(is_responded=True)
    mark_as_responded.short_description = "Mark selected contacts as responded"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'company', 'content']
    list_editable = ['is_featured', 'is_active']
    
    fieldsets = (
        ('Person Information', {
            'fields': ('name', 'position', 'company', 'photo')
        }),
        ('Testimonial', {
            'fields': ('content', 'rating')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
    )
    
    def get_photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.photo.url)
        return "No photo"
    get_photo_preview.short_description = "Photo Preview"

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'max_participants', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'key_points')
        }),
        ('Workshop Details', {
            'fields': ('duration', 'max_participants', 'price')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
    )
