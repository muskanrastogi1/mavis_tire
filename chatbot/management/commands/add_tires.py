from django.core.management.base import BaseCommand
from chatbot.models import TireBrand, TireSize

class Command(BaseCommand):
    help = 'Adds sample tire brands and sizes to the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        TireSize.objects.all().delete()
        TireBrand.objects.all().delete()

        # Add tire brands
        brands = [
            {
                'name': 'Michelin',
                'description': 'Premium tires known for longevity and performance'
            },
            {
                'name': 'Goodyear',
                'description': 'Reliable all-season tires with excellent traction'
            },
            {
                'name': 'Bridgestone',
                'description': 'High-performance tires with great handling'
            }
        ]

        for brand_data in brands:
            brand = TireBrand.objects.create(**brand_data)
            self.stdout.write(self.style.SUCCESS(f'Added brand: {brand.name}'))

            # Add sizes for each brand
            if brand.name == 'Michelin':
                sizes = [
                    {
                        'size': '205/55R16',
                        'price_range': '$120-$150',
                        'features': 'All-season performance, long tread life, fuel efficient'
                    },
                    {
                        'size': '225/45R17',
                        'price_range': '$150-$180',
                        'features': 'Sport performance, excellent handling, responsive'
                    }
                ]
            elif brand.name == 'Goodyear':
                sizes = [
                    {
                        'size': '215/60R16',
                        'price_range': '$110-$140',
                        'features': 'All-season traction, comfortable ride, durable'
                    },
                    {
                        'size': '235/55R18',
                        'price_range': '$160-$190',
                        'features': 'Premium touring, quiet ride, long-lasting'
                    }
                ]
            else:  # Bridgestone
                sizes = [
                    {
                        'size': '225/50R17',
                        'price_range': '$130-$160',
                        'features': 'High-performance, excellent grip, sporty handling'
                    },
                    {
                        'size': '245/45R19',
                        'price_range': '$170-$200',
                        'features': 'Ultra-high performance, maximum grip, responsive'
                    }
                ]

            for size_data in sizes:
                TireSize.objects.create(brand=brand, **size_data)
                self.stdout.write(self.style.SUCCESS(f'Added size: {brand.name} {size_data["size"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully added all tire brands and sizes!')) 