from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from .models import SiteSettings, Service, Program, BlogPost, Contact, Testimonial, Workshop, HomePage, MyStory, InsightsPage

def get_site_settings():
    """Get or create site settings"""
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'site_title': 'Srinikethan - Financial Coach',
            'hero_title': 'Finance Forward With Srinikethan!',
            'about_title': 'Financial Coach, Educator, & Author',
            'about_content': """I'm Srinikethan, Founder & CEO of my financial consulting firm, on a mission since 2009 to help professionals and families take control of their finances. With over 15 years of experience, I simplify financial management through actionable strategies, interactive workshops, and one-on-one consultations—empowering clients to optimize investments, plan for retirement, and build lasting wealth.

My journey began with personal financial setbacks that taught me the value of informed decision-making, and today, I use those lessons to guide others through India's complex financial landscape. If you're ready to transform your relationship with money and achieve your goals with clarity and confidence, let's connect."""
        }
    )
    return settings

def get_homepage_content():
    """Get or create homepage content"""
    homepage, created = HomePage.objects.get_or_create(pk=1)
    return homepage

def get_mystory_content():
    """Get or create my story content"""
    mystory, created = MyStory.objects.get_or_create(pk=1)
    return mystory

def get_insights_content():
    """Get or create insights page content"""
    insights, created = InsightsPage.objects.get_or_create(pk=1)
    return insights

def home(request):
    settings = get_site_settings()
    homepage = get_homepage_content()
    services = Service.objects.filter(is_active=True).order_by('order', 'title')
    programs = Program.objects.filter(is_active=True).order_by('order', 'name')
    testimonials = Testimonial.objects.filter(is_active=True, is_featured=True)[:3]
    latest_posts = BlogPost.objects.filter(is_published=True)[:3]
    
    context = {
        'settings': settings,
        'homepage': homepage,
        'services': services,
        'programs': programs,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    settings = get_site_settings()
    mystory = get_mystory_content()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    
    context = {
        'settings': settings,
        'mystory': mystory,
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/about.html', context)

def services(request):
    settings = get_site_settings()
    services = Service.objects.filter(is_active=True).order_by('order', 'title')
    programs = Program.objects.filter(is_active=True).order_by('order', 'name')
    workshops = Workshop.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
        'services': services,
        'programs': programs,
        'workshops': workshops,
    }
    return render(request, 'portfolio/services.html', context)

def insights(request):
    settings = get_site_settings()
    insights_content = get_insights_content()
    latest_posts = BlogPost.objects.filter(is_published=True)[:4]
    
    context = {
        'settings': settings,
        'insights': insights_content,
        'latest_posts': latest_posts,
    }
    return render(request, 'portfolio/insights.html', context)

def blog(request):
    settings = get_site_settings()
    posts_list = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'settings': settings,
        'posts': posts,
        'featured_posts': featured_posts,
    }
    return render(request, 'portfolio/blog.html', context)

def blog_detail(request, slug):
    settings = get_site_settings()
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(pk=post.pk)[:3]
    
    context = {
        'settings': settings,
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'portfolio/blog_detail.html', context)

def contact(request):
    settings = get_site_settings()
    
    if request.method == 'POST':
        # Handle contact form submission
        contact = Contact(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone', ''),
            company=request.POST.get('company', ''),
            inquiry_type=request.POST.get('inquiry_type', 'general'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message'),
        )
        contact.save()
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    context = {
        'settings': settings,
        'inquiry_types': Contact.INQUIRY_TYPES,
    }
    return render(request, 'portfolio/contact.html', context)
