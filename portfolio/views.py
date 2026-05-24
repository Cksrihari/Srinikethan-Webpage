from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from two_factor.views import SetupView
from .models import SiteSettings, Service, Program, BlogPost, Contact, Testimonial, Workshop, HomePage, MyStory, InsightsPage, ServicesPage, BlogPage


class UpdateTwoFactorView(SetupView):
    """
    Identical to the stock SetupView but skips the 'already configured'
    redirect so an existing user can replace their device.
    """
    def get(self, request, *args, **kwargs):
        # Bypass the parent's early-exit when a device already exists.
        from formtools.wizard.views import SessionWizardView
        return SessionWizardView.get(self, request, *args, **kwargs)


@login_required
def post_login_redirect(request):
    """
    Called as LOGIN_REDIRECT_URL after login or after the 2FA setup wizard.
    - Staff with no OTP device: first visit → force setup; subsequent visit
      (i.e. they cancelled setup) → log them out so they can't bypass 2FA.
    - Staff with a device → go to admin.
    """
    from django_otp import devices_for_user
    from django.contrib.auth import logout
    if request.user.is_staff and not list(devices_for_user(request.user)):
        if request.session.get('2fa_setup_initiated'):
            # User cancelled setup — log out to prevent 2FA bypass
            logout(request)
            from django.contrib import messages
            messages.warning(request, 'Two-factor authentication is required. Please complete the setup to access the admin.')
            return redirect('/account/login/')
        # First time: send to setup and mark session so we detect cancel
        request.session['2fa_setup_initiated'] = True
        return redirect('/account/two_factor/setup/')
    request.session.pop('2fa_setup_initiated', None)
    return redirect('/admin/')

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

def get_services_content():
    """Get or create services page content"""
    services_page, created = ServicesPage.objects.get_or_create(pk=1)
    return services_page

def get_blog_content():
    """Get or create blog page content"""
    blog_page, created = BlogPage.objects.get_or_create(pk=1)
    return blog_page

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
    services_page = get_services_content()
    services = Service.objects.filter(is_active=True).order_by('order', 'title')
    programs = Program.objects.filter(is_active=True).order_by('order', 'name')
    workshops = Workshop.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
        'services_page': services_page,
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
    blog_page = get_blog_content()
    posts_list = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    featured_posts = BlogPost.objects.filter(is_published=True, is_featured=True)[:3]
    
    paginator = Paginator(posts_list, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'settings': settings,
        'blog_page': blog_page,
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
