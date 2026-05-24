from django.core.management.base import BaseCommand
from portfolio.models import HomePage, MyStory

class Command(BaseCommand):
    help = 'Initialize homepage and my story content with default values'

    def handle(self, *args, **options):
        # Create or get homepage content
        homepage, created = HomePage.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created HomePage content with default values')
            )
        else:
            self.stdout.write(
                self.style.WARNING('HomePage content already exists')
            )

        # Create or get my story content
        mystory, created = MyStory.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created MyStory content with default values')
            )
        else:
            self.stdout.write(
                self.style.WARNING('MyStory content already exists')
            )

        self.stdout.write(
            self.style.SUCCESS('Content initialization complete. You can now edit content through the Django admin at /admin/')
        )