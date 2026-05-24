from django.core.management.base import BaseCommand
from portfolio.models import Service, Program

class Command(BaseCommand):
    help = 'Populate services and programs with wealth management expertise'

    def handle(self, *args, **options):
        # Create or update services
        services_data = [
            {
                'title': 'Investment Management',
                'description': 'Strategic portfolio construction and management tailored to your risk tolerance and financial objectives. We utilize modern portfolio theory and institutional-quality investment strategies.',
                'icon': '📊',
                'order': 1
            },
            {
                'title': 'Financial Planning',
                'description': 'Comprehensive financial planning to help you achieve your short-term and long-term financial goals. We create detailed roadmaps for your financial success.',
                'icon': '🎯',
                'order': 2
            },
            {
                'title': 'Estate Planning',
                'description': 'Protect your legacy and ensure smooth wealth transfer to future generations with strategic estate planning. Minimize taxes and maximize family wealth preservation.',
                'icon': '🏠',
                'order': 3
            },
            {
                'title': 'Risk Management',
                'description': 'Comprehensive insurance solutions and risk mitigation strategies to protect your wealth and family. Safeguard against unexpected life events.',
                'icon': '🛡️',
                'order': 4
            },
            {
                'title': 'Education Funding',
                'description': 'Strategic planning for education expenses with tax-efficient savings and investment strategies. Secure your children\'s educational future.',
                'icon': '🎓',
                'order': 5
            },
            {
                'title': 'Retirement Planning',
                'description': 'Build a secure retirement with comprehensive strategies for income replacement and lifestyle maintenance. Plan for financial independence.',
                'icon': '🏖️',
                'order': 6
            },
            {
                'title': 'Tax Optimization',
                'description': 'Advanced tax planning strategies to minimize your tax burden while maximizing wealth accumulation. Strategic timing and structure optimization.',
                'icon': '💰',
                'order': 7
            },
            {
                'title': 'Corporate Benefits',
                'description': 'Maximize your company benefits including stock options, 401(k) plans, and executive compensation packages. Optimize your total compensation.',
                'icon': '🏢',
                'order': 8
            }
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.title}')
            else:
                # Update existing service
                for key, value in service_data.items():
                    setattr(service, key, value)
                service.save()
                self.stdout.write(f'Updated service: {service.title}')

        # Create or update programs
        programs_data = [
            {
                'name': 'Wealth Building Masterclass',
                'description': 'Comprehensive 8-week program covering investment strategies, portfolio management, and wealth accumulation techniques for high-achievers.',
                'duration': '8 weeks',
                'price': 2497.00,
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Retirement Planning Workshop',
                'description': 'Interactive workshop focusing on retirement income planning, Social Security optimization, and distribution strategies.',
                'duration': '2 days',
                'price': 497.00,
                'is_featured': False,
                'order': 2
            },
            {
                'name': 'Estate Planning Essentials',
                'description': 'Learn the fundamentals of estate planning, including wills, trusts, and tax-efficient wealth transfer strategies.',
                'duration': '1 day',
                'price': 297.00,
                'is_featured': False,
                'order': 3
            },
            {
                'name': 'Executive Financial Strategy',
                'description': 'Specialized program for executives and business owners covering stock options, deferred compensation, and business succession planning.',
                'duration': '6 weeks',
                'price': 4997.00,
                'is_featured': True,
                'order': 4
            }
        ]

        for program_data in programs_data:
            program, created = Program.objects.get_or_create(
                name=program_data['name'],
                defaults=program_data
            )
            if created:
                self.stdout.write(f'Created program: {program.name}')
            else:
                # Update existing program
                for key, value in program_data.items():
                    setattr(program, key, value)
                program.save()
                self.stdout.write(f'Updated program: {program.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated wealth management expertise content')
        )