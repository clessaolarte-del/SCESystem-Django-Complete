from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from equipment.models import Equipment


class Command(BaseCommand):
    help = "Seed sample data"

    def handle(self, *args, **options):
        if User.objects.filter(username="student").exists():
            return

        User.objects.create_user(username="student", email="student@example.com", password="student123")
        User.objects.create_superuser(username="admin", email="admin@example.com", password="admin123")

        equipment_data = [
            (
                "Laptop (Dell)",
                "Laptop",
                "IT Office",
                "Good",
                5,
                5,
                "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=500&h=400&q=80",
                "Dell laptop for academic and project use.",
            ),
            (
                "Projector",
                "Projector",
                "AV Room",
                "Good",
                3,
                3,
                "https://images.unsplash.com/photo-1516321165247-4aa89a48be28?auto=format&fit=crop&w=500&h=400&q=80",
                "Projector for classroom presentations.",
            ),
            (
                "Camera (Canon)",
                "Camera",
                "IT Office",
                "Good",
                4,
                4,
                "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=500&h=400&q=80",
                "Canon camera for media assignments.",
            ),
            (
                "Tripod",
                "Accessories",
                "IT Office",
                "Good",
                6,
                6,
                "https://images.unsplash.com/photo-1610827033614-f20a73aee18c?auto=format&fit=crop&w=500&h=400&q=80",
                "Adjustable tripod for camera support.",
            ),
            (
                "Microphone",
                "Audio",
                "Audio Room",
                "Good",
                5,
                5,
                "https://images.unsplash.com/photo-1511379938547-c1f69419868d?auto=format&fit=crop&w=500&h=400&q=80",
                "Portable microphone for presentations.",
            ),
            (
                "Speaker",
                "Audio",
                "Audio Room",
                "Good",
                4,
                4,
                "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=500&h=400&q=80",
                "High-quality classroom speaker.",
            ),
            (
                "Tablet",
                "Tablet",
                "Library",
                "Good",
                4,
                4,
                "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=500&h=400&q=80",
                "Tablet for class notes and research.",
            ),
            (
                "Whiteboard",
                "Office",
                "Classroom 1",
                "Good",
                2,
                2,
                "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&h=400&q=80",
                "Portable whiteboard for team activities.",
            ),
        ]

        for item in equipment_data:
            Equipment.objects.create(
                name=item[0],
                category=item[1],
                location=item[2],
                condition=item[3],
                quantity=item[4],
                available_quantity=item[5],
                image_url=item[6],
                description=item[7],
            )

        self.stdout.write(self.style.SUCCESS("Sample data loaded successfully."))
