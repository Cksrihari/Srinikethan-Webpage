from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import reverse
from .models import (
    SiteSettings, Service, Program, BlogPost, Contact,
    Testimonial, Workshop, HomePage, MyStory,
    InsightsPage, ServicesPage, BlogPage,
)

# ── Branding (jazzmin picks these up too) ─────────────────────────────────────
admin.site.site_header = "Srinikethan - Content Manager"
admin.site.site_title  = "Srinikethan Admin"
admin.site.index_title = "Website Dashboard"


# ── Superuser-only mixin for User / Group management ─────────────────────────
class SuperuserOnlyAdmin(admin.ModelAdmin):
    """Only superusers may view or change this model."""

    def has_module_perms(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# ── User & Group – superuser only ────────────────────────────────────────────
class SuperuserUserAdmin(SuperuserOnlyAdmin, UserAdmin):
    pass


class SuperuserGroupAdmin(SuperuserOnlyAdmin, GroupAdmin):
    pass


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, SuperuserUserAdmin)
admin.site.register(Group, SuperuserGroupAdmin)


# ── Helper mixin: single-instance pages skip the list view ───────────────────
class SingleInstanceAdmin(admin.ModelAdmin):
    """
    For models that only ever have one row (HomePage, MyStory, etc.)
    clicking the model link goes straight to the edit form.
    """
    def changelist_view(self, request, extra_context=None):
        obj, _ = self.model.objects.get_or_create(pk=1)
        return redirect(
            reverse(
                f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change",
                args=[obj.pk],
            )
        )

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        if "_continue" not in request.POST and "_addanother" not in request.POST:
            from django.contrib import messages
            messages.success(request, f'"{obj}" saved successfully.')
            return redirect(request.path)
        return super().response_change(request, obj)

# ── Site Settings ─────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(SingleInstanceAdmin):
    save_on_top = True
    fieldsets = (
        ("🌐  Site Information", {
            "description": "The site title and main hero text shown at the top of the website.",
            "fields": ("site_title", "hero_title", "hero_subtitle", "about_title", "about_content"),
        }),
        ("📞  Contact Details", {
            "description": "Your contact information shown in the footer and contact page.",
            "fields": ("contact_email", "contact_phone", "contact_address"),
        }),
        ("🔗  Social Media Links", {
            "description": "Paste the full URL to each of your social media profiles.",
            "fields": ("linkedin_url", "twitter_url", "facebook_url"),
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ["title", "icon", "order", "is_active"]
    list_filter   = ["is_active"]
    search_fields = ["title", "description"]
    list_editable = ["order", "is_active"]
    ordering      = ["order", "title"]
    fieldsets = (
        ("Service Details", {
            "description": "Fill in the name and description for this service card.",
            "fields": ("title", "description", "icon"),
        }),
        ("Display Settings", {
            "description": '"Order" controls position (lower = appears first). Untick "Active" to hide without deleting.',
            "fields": ("order", "is_active"),
        }),
    )

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display  = ["name", "duration", "price", "is_featured", "is_active", "order"]
    list_filter   = ["is_featured", "is_active"]
    search_fields = ["name", "description"]
    list_editable = ["is_featured", "is_active", "order"]
    ordering      = ["order", "name"]
    fieldsets = (
        ("Program Details", {
            "fields": ("name", "description", "duration", "price"),
        }),
        ("Display Settings", {
            "description": 'Tick "Featured" to highlight this program. "Order" controls position.',
            "fields": ("is_featured", "order", "is_active"),
        }),
    )

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display        = ["title", "status_badge", "is_featured", "created_at", "published_at"]
    list_filter         = ["is_published", "is_featured", "created_at"]
    search_fields       = ["title", "content", "tags"]
    list_editable       = ["is_featured"]
    readonly_fields     = ["published_at", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("title",)}
    save_on_top         = True
    fieldsets = (
        ("✍️  Post Content", {
            "description": "Write the title, main body, and a short excerpt (used in previews and social sharing).",
            "fields": ("title", "slug", "excerpt", "content", "featured_image"),
        }),
        ("📢  Publishing", {
            "description": 'Tick "Published" when the post is ready to go live.',
            "fields": ("is_published", "is_featured", "author", "published_at"),
        }),
        ("🏷️  Tags & SEO", {
            "description": "Comma-separated tags help readers find related posts. Meta description (max 160 chars) is used by search engines.",
            "fields": ("tags", "meta_description"),
            "classes": ("collapse",),
        }),
        ("ℹ️  Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def status_badge(self, obj):
        if obj.is_published:
            return format_html('<span class="sk-badge sk-badge-green">Published</span>')
        return format_html('<span class="sk-badge sk-badge-yellow">Draft</span>')
    status_badge.short_description = "Status"

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ["full_name", "email", "inquiry_type", "subject_short", "status_badge", "is_read", "is_responded", "created_at"]
    list_filter   = ["inquiry_type", "is_read", "is_responded", "created_at"]
    search_fields = ["first_name", "last_name", "email", "subject", "message"]
    list_editable = ["is_read", "is_responded"]
    readonly_fields = ["created_at"]
    ordering      = ["-created_at"]
    fieldsets = (
        ("👤  Contact Information", {
            "fields": ("first_name", "last_name", "email", "phone", "company"),
        }),
        ("💬  Enquiry", {
            "fields": ("inquiry_type", "subject", "message"),
        }),
        ("✅  Status & Notes", {
            "description": "Mark as read once reviewed, and responded once you have replied.",
            "fields": ("is_read", "is_responded", "notes", "created_at"),
        }),
    )
    actions = ["mark_as_read", "mark_as_responded"]

    def subject_short(self, obj):
        s = obj.subject or ""
        return s[:60] + ("…" if len(s) > 60 else "")
    subject_short.short_description = "Subject"

    def status_badge(self, obj):
        if not obj.is_read:
            return format_html('<span class="sk-badge sk-badge-red">Unread</span>')
        if not obj.is_responded:
            return format_html('<span class="sk-badge sk-badge-yellow">Pending Reply</span>')
        return format_html('<span class="sk-badge sk-badge-green">Responded</span>')
    status_badge.short_description = "Status"

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "✔ Mark selected as Read"

    def mark_as_responded(self, request, queryset):
        queryset.update(is_responded=True)
    mark_as_responded.short_description = "✔ Mark selected as Responded"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ["name", "company", "star_rating", "is_featured", "is_active"]
    list_filter   = ["rating", "is_featured", "is_active"]
    search_fields = ["name", "company", "content"]
    list_editable = ["is_featured", "is_active"]
    fieldsets = (
        ("👤  Person", {
            "fields": ("name", "position", "company", "photo"),
        }),
        ("💬  Testimonial", {
            "fields": ("content", "rating"),
        }),
        ("⚙️  Visibility", {
            "description": 'Tick "Featured" to show in the homepage success-stories section.',
            "fields": ("is_featured", "is_active"),
        }),
    )

    def star_rating(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html('<span style="color:#c9a84c;font-size:1rem;">{}</span>', stars)
    star_rating.short_description = "Rating"

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display  = ["title", "duration", "max_participants", "price", "is_active"]
    list_filter   = ["is_active"]
    search_fields = ["title", "description"]
    list_editable = ["is_active"]
    fieldsets = (
        ("Workshop Details", {
            "fields": ("title", "description", "key_points"),
        }),
        ("Logistics", {
            "fields": ("duration", "max_participants", "price"),
        }),
        ("⚙️  Visibility", {
            "fields": ("is_active",),
        }),
    )

@admin.register(HomePage)
class HomePageAdmin(SingleInstanceAdmin):
    readonly_fields = ["updated_at"]
    save_on_top = True
    fieldsets = (
        ("🖼️  Hero Section", {
            "description": "The very first thing visitors see when they arrive on the homepage.",
            "fields": ("welcome_label", "welcome_title", "welcome_subtitle", "profile_photo", "scroll_prompt_text"),
        }),
        ("💭  Philosophy Section", {
            "description": 'The "My Philosophy" block that follows the hero.',
            "fields": (
                "philosophy_title", "philosophy_subtitle",
                "philosophy_highlight_1", "philosophy_highlight_2",
                "philosophy_highlight_3", "philosophy_highlight_4",
            ),
        }),
        ("🎯  Expertise Section", {
            "description": "The section showcasing your areas of expertise.",
            "fields": ("expertise_label", "expertise_title", "expertise_subtitle"),
        }),
        ("🚀  Financial Journeys Section", {
            "description": "The coaching-programme / journey cards section.",
            "fields": ("journeys_label", "journeys_title", "journeys_subtitle"),
        }),
        ("⭐  Success Stories Section", {
            "fields": ("success_stories_title", "success_stories_subtitle"),
        }),
        ("📚  Knowledge Hub Section", {
            "fields": ("knowledge_hub_label", "knowledge_hub_title", "knowledge_hub_subtitle"),
        }),
        ("🔘  Call-to-Action Buttons", {
            "description": "The two buttons in the hero section.",
            "fields": (
                "primary_cta_text", "primary_cta_url",
                "secondary_cta_text", "secondary_cta_url",
            ),
        }),
        ("ℹ️  Last Updated", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(ServicesPage)
class ServicesPageAdmin(SingleInstanceAdmin):
    readonly_fields = ["updated_at"]
    save_on_top = True
    fieldsets = (
        ("📄  Page Header", {
            "description": "The banner text at the very top of the Services page.",
            "fields": ("page_label", "page_title", "page_subtitle"),
        }),
        ("🏦  Core Services Section", {
            "fields": ("core_services_title", "core_services_subtitle"),
        }),
        ("💎  Specialised Solutions Section", {
            "fields": ("specialized_title", "specialized_subtitle"),
        }),
        ("🔄  Our Process Section", {
            "fields": ("process_title", "process_subtitle"),
        }),
        ("🔘  Call to Action", {
            "description": "The bottom block encouraging visitors to get in touch.",
            "fields": ("cta_title", "cta_description", "cta_primary_text", "cta_secondary_text"),
        }),
        ("ℹ️  Last Updated", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(BlogPage)
class BlogPageAdmin(SingleInstanceAdmin):
    readonly_fields = ["updated_at"]
    save_on_top = True
    fieldsets = (
        ("📄  Page Header", {
            "description": "The banner text at the top of the Blog index page.",
            "fields": ("page_label", "page_title", "page_subtitle"),
        }),
        ("📌  Featured Articles Section", {
            "fields": ("featured_posts_title", "featured_posts_subtitle"),
        }),
        ("📋  All Articles Section", {
            "fields": ("all_posts_title", "all_posts_subtitle"),
        }),
        ("🔘  Call to Action", {
            "fields": ("cta_title", "cta_description", "cta_button_text", "cta_button_url"),
        }),
        ("ℹ️  Last Updated", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(MyStory)
class MyStoryAdmin(SingleInstanceAdmin):
    readonly_fields = ["updated_at"]
    save_on_top = True
    fieldsets = (
        ("📄  Page Header", {
            "description": "The title and opening paragraph of the My Story page.",
            "fields": ("page_title", "page_subtitle", "intro_text"),
        }),
        ("📅  Chapter 1 – Early Foundation", {
            "fields": ("chapter_1_number", "chapter_1_title", "chapter_1_period", "chapter_1_content"),
        }),
        ("📅  Chapter 2 – Professional Growth", {
            "fields": ("chapter_2_number", "chapter_2_title", "chapter_2_period", "chapter_2_content"),
        }),
        ("📅  Chapter 3 – Market Expertise", {
            "fields": ("chapter_3_number", "chapter_3_title", "chapter_3_period", "chapter_3_content"),
        }),
        ("📅  Chapter 4 – Today & Beyond", {
            "fields": ("chapter_4_number", "chapter_4_title", "chapter_4_period", "chapter_4_content"),
        }),
        ("🎯  Mission & Personal Note", {
            "fields": ("mission_title", "mission_text", "personal_note"),
        }),
        ("ℹ️  Last Updated", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )

@admin.register(InsightsPage)
class InsightsPageAdmin(SingleInstanceAdmin):
    readonly_fields = ["updated_at"]
    save_on_top = True
    fieldsets = (
        ("📄  Page Header", {
            "fields": ("page_title", "page_subtitle"),
        }),
        ("🦸  Hero Section", {
            "fields": ("hero_title", "hero_description"),
        }),
        ("⭐  Featured Insight", {
            "description": "The large featured insight card at the top of the page.",
            "fields": ("featured_title", "featured_excerpt", "featured_content", "featured_image_alt"),
        }),
        ("⚡  Quick Insights (4 Cards)", {
            "description": "The four small insight cards.",
            "fields": (
                "quick_insights_title", "quick_insights_subtitle",
                "insight_1_title", "insight_1_content",
                "insight_2_title", "insight_2_content",
                "insight_3_title", "insight_3_content",
                "insight_4_title", "insight_4_content",
            ),
        }),
        ("📰  Latest Articles Section", {
            "fields": ("latest_articles_title", "latest_articles_subtitle"),
        }),
        ("📧  Newsletter Section", {
            "fields": ("newsletter_title", "newsletter_description"),
        }),
        ("🔘  Call to Action", {
            "fields": ("cta_title", "cta_description", "cta_button_text", "cta_button_url"),
        }),
        ("ℹ️  Last Updated", {
            "fields": ("updated_at",),
            "classes": ("collapse",),
        }),
    )
