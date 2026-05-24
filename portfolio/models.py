from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=100, default="Srinikethan - Financial Coach")
    hero_title = models.CharField(max_length=200, default="Finance Forward With Srinikethan!")
    hero_subtitle = models.TextField(blank=True)
    about_title = models.CharField(max_length=100, default="Financial Coach, Educator, & Author")
    about_content = models.TextField()
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_address = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError("Only one SiteSettings instance is allowed")
        return super().save(*args, **kwargs)

class HomePage(models.Model):
    """Model for homepage content that can be updated through admin"""
    
    # Welcome Banner Section
    welcome_title = models.CharField(
        max_length=200, 
        default="Your Financial Growth Partner",
        help_text="Main title displayed in the welcome banner"
    )
    welcome_subtitle = models.TextField(
        default="Empowering you to achieve financial independence through smart planning and strategic growth.",
        help_text="Subtitle text under the welcome title"
    )
    profile_photo = models.ImageField(
        upload_to='homepage/', 
        blank=True, 
        null=True,
        help_text="Profile photo displayed in the welcome banner"
    )
    
    # Philosophy Section
    philosophy_title = models.CharField(
        max_length=200,
        default="My Philosophy",
        help_text="Title for the philosophy section"
    )
    philosophy_subtitle = models.CharField(
        max_length=300,
        default="Building wealth is not about luck—it's about having the right strategy, consistent execution, and a trusted guide.",
        help_text="Philosophy subtitle"
    )
    philosophy_highlight_1 = models.CharField(max_length=100, default="Personalized Strategies")
    philosophy_highlight_2 = models.CharField(max_length=100, default="Data-Driven Insights") 
    philosophy_highlight_3 = models.CharField(max_length=100, default="Long-term Success")
    philosophy_highlight_4 = models.CharField(max_length=100, default="Continuous Support")
    
    # Expertise Section
    expertise_title = models.CharField(
        max_length=200,
        default="Expertise Areas",
        help_text="Title for the expertise section"
    )
    expertise_subtitle = models.TextField(
        default="Comprehensive financial solutions tailored to your unique goals and circumstances.",
        help_text="Subtitle for expertise section"
    )
    
    # Success Stories Section
    success_stories_title = models.CharField(
        max_length=200,
        default="Success Stories",
        help_text="Title for success stories section"
    )
    success_stories_subtitle = models.TextField(
        default="Real transformations from clients who trusted the journey.",
        help_text="Subtitle for success stories section"
    )
    
    # Knowledge Hub Section
    knowledge_hub_title = models.CharField(
        max_length=200,
        default="Knowledge Hub",
        help_text="Title for knowledge hub section"
    )
    knowledge_hub_subtitle = models.TextField(
        default="Latest insights, strategies, and market perspectives to keep you informed.",
        help_text="Subtitle for knowledge hub section"
    )
    
    # CTA Buttons
    primary_cta_text = models.CharField(max_length=50, default="Start Your Journey")
    primary_cta_url = models.CharField(max_length=200, default="/contact/")
    secondary_cta_text = models.CharField(max_length=50, default="Explore Expertise")
    secondary_cta_url = models.CharField(max_length=200, default="#expertise")
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Homepage Content"
        verbose_name_plural = "Homepage Content"
    
    def __str__(self):
        return "Homepage Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and HomePage.objects.exists():
            raise ValueError("Only one HomePage instance is allowed")
        return super().save(*args, **kwargs)

class MyStory(models.Model):
    """Model for 'My Story' page content that can be updated through admin"""
    
    # Page Header
    page_title = models.CharField(
        max_length=200,
        default="My Story",
        help_text="Main page title"
    )
    page_subtitle = models.TextField(
        default="Every great journey begins with a single step. Here's how my passion for financial empowerment began.",
        help_text="Page subtitle/introduction"
    )
    
    # Story Introduction
    intro_text = models.TextField(
        default="My path to becoming a financial growth partner wasn't traditional, but it was authentic. Each chapter of my life has shaped my understanding of what it truly means to achieve financial independence.",
        help_text="Introduction text for the story"
    )
    
    # Life Chapters (Timeline)
    chapter_1_number = models.CharField(max_length=10, default="01")
    chapter_1_title = models.CharField(max_length=100, default="Early Foundation")
    chapter_1_period = models.CharField(max_length=50, default="2010-2014")
    chapter_1_content = models.TextField(
        default="Started my journey understanding the basics of personal finance and investment principles.",
        help_text="Content for chapter 1"
    )
    
    chapter_2_number = models.CharField(max_length=10, default="02")
    chapter_2_title = models.CharField(max_length=100, default="Professional Growth")
    chapter_2_period = models.CharField(max_length=50, default="2015-2018")
    chapter_2_content = models.TextField(
        default="Developed expertise in financial planning while helping others achieve their goals.",
        help_text="Content for chapter 2"
    )
    
    chapter_3_number = models.CharField(max_length=10, default="03")
    chapter_3_title = models.CharField(max_length=100, default="Market Expertise")
    chapter_3_period = models.CharField(max_length=50, default="2019-2022")
    chapter_3_content = models.TextField(
        default="Navigated market volatility and economic challenges, refining strategies for sustainable growth.",
        help_text="Content for chapter 3"
    )
    
    chapter_4_number = models.CharField(max_length=10, default="04")
    chapter_4_title = models.CharField(max_length=100, default="Today & Beyond")
    chapter_4_period = models.CharField(max_length=50, default="2023-Present")
    chapter_4_content = models.TextField(
        default="Continuing to innovate and guide clients toward financial independence with proven strategies.",
        help_text="Content for chapter 4"
    )
    
    # Mission Statement
    mission_title = models.CharField(
        max_length=200,
        default="Mission & Vision",
        help_text="Title for mission section"
    )
    mission_text = models.TextField(
        default="My mission is simple: to democratize financial growth and make wealth-building strategies accessible to everyone, regardless of their starting point.",
        help_text="Mission statement text"
    )
    
    # Personal Touch
    personal_note = models.TextField(
        default="When I'm not analyzing markets or developing strategies, you'll find me reading, traveling, or exploring new technologies that can enhance financial planning.",
        help_text="Personal note to add authenticity"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "My Story Content"
        verbose_name_plural = "My Story Content"
    
    def __str__(self):
        return "My Story Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and MyStory.objects.exists():
            raise ValueError("Only one MyStory instance is allowed")
        return super().save(*args, **kwargs)

class InsightsPage(models.Model):
    """Model for insights page content that can be updated through admin"""
    
    # Page Header
    page_title = models.CharField(
        max_length=200,
        default="Financial Insights",
        help_text="Main page title"
    )
    page_subtitle = models.TextField(
        default="Expert analysis, market trends, and strategic insights to enhance your financial journey.",
        help_text="Page subtitle/introduction"
    )
    
    # Hero Section
    hero_title = models.CharField(
        max_length=300,
        default="Navigate Markets with Confidence",
        help_text="Main hero section title"
    )
    hero_description = models.TextField(
        default="Stay ahead of market trends with expert analysis, actionable insights, and proven strategies that drive real financial growth.",
        help_text="Hero section description"
    )
    
    # Featured Insight
    featured_title = models.CharField(
        max_length=200,
        default="Market Outlook 2024",
        help_text="Featured insight title"
    )
    featured_excerpt = models.TextField(
        default="Understanding the key economic indicators and investment opportunities that will shape the financial landscape this year.",
        help_text="Featured insight excerpt"
    )
    featured_content = models.TextField(
        default="The financial markets are experiencing unprecedented shifts...",
        help_text="Full content for featured insight"
    )
    featured_image_alt = models.CharField(
        max_length=200,
        default="Market analysis chart",
        help_text="Alt text for featured image"
    )
    
    # Quick Insights Section
    quick_insights_title = models.CharField(
        max_length=200,
        default="Quick Market Insights",
        help_text="Title for quick insights section"
    )
    
    # Insight 1
    insight_1_title = models.CharField(
        max_length=150,
        default="Diversification Strategies",
        help_text="First quick insight title"
    )
    insight_1_content = models.TextField(
        default="Learn how to spread risk across different asset classes for more stable long-term returns.",
        help_text="First quick insight content"
    )
    
    # Insight 2
    insight_2_title = models.CharField(
        max_length=150,
        default="Tax Optimization Tips",
        help_text="Second quick insight title"
    )
    insight_2_content = models.TextField(
        default="Maximize your after-tax returns with strategic planning and smart investment timing.",
        help_text="Second quick insight content"
    )
    
    # Insight 3
    insight_3_title = models.CharField(
        max_length=150,
        default="Economic Indicators",
        help_text="Third quick insight title"
    )
    insight_3_content = models.TextField(
        default="Key metrics to watch that signal market direction and investment opportunities.",
        help_text="Third quick insight content"
    )
    
    # Insight 4
    insight_4_title = models.CharField(
        max_length=150,
        default="Risk Management",
        help_text="Fourth quick insight title"
    )
    insight_4_content = models.TextField(
        default="Protect your portfolio with proven risk assessment and mitigation strategies.",
        help_text="Fourth quick insight content"
    )
    
    # Newsletter Section
    newsletter_title = models.CharField(
        max_length=200,
        default="Stay Updated",
        help_text="Newsletter signup section title"
    )
    newsletter_description = models.TextField(
        default="Get weekly insights delivered to your inbox. Market analysis, investment tips, and exclusive strategies.",
        help_text="Newsletter signup description"
    )
    
    # CTA Section
    cta_title = models.CharField(
        max_length=200,
        default="Ready to Apply These Insights?",
        help_text="Call to action title"
    )
    cta_description = models.TextField(
        default="Transform market knowledge into personal wealth. Let's discuss your financial strategy.",
        help_text="Call to action description"
    )
    cta_button_text = models.CharField(
        max_length=50,
        default="Schedule Consultation",
        help_text="CTA button text"
    )
    cta_button_url = models.CharField(
        max_length=200,
        default="/contact/",
        help_text="CTA button URL"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Insights Page Content"
        verbose_name_plural = "Insights Page Content"
    
    def __str__(self):
        return "Insights Page Content"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and InsightsPage.objects.exists():
            raise ValueError("Only one InsightsPage instance is allowed")
        return super().save(*args, **kwargs)

class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or emoji")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return self.title

class Program(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, help_text="Brief description for previews")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

class Contact(models.Model):
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('consultation', 'Consultation Request'),
        ('workshop', 'Workshop Inquiry'),
        ('speaking', 'Speaking Engagement'),
        ('other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    key_points = models.TextField(help_text="Key learning points, one per line")
    duration = models.CharField(max_length=50)
    max_participants = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
