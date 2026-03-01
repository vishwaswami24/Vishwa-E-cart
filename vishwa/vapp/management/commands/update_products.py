from django.core.management.base import BaseCommand
from vapp.models import Product

class Command(BaseCommand):
    help = 'Updates existing products with stock and brand information'

    def handle(self, *args, **options):
        self.stdout.write('Updating products...')
        
        products_without_stock = Product.objects.filter(stock=0)
        count = products_without_stock.update(stock=100)
        self.stdout.write(f'Updated {count} products with default stock (100)')
        
        brand_keywords = {
            'Bajaj': ['bajaj'],
            'Havells': ['havells'],
            'Philips': ['philips'],
            'Crompton': ['crompton'],
            'Orient': ['orient'],
            'Usha': ['usha'],
            'Syska': ['syska'],
        }
        
        updated_count = 0
        for product in Product.objects.filter(brand=''):
            brand_found = False
            for brand, keywords in brand_keywords.items():
                if any(keyword in product.name.lower() for keyword in keywords):
                    product.brand = brand
                    product.save()
                    brand_found = True
                    updated_count += 1
                    break
            
            if not brand_found:
                product.brand = 'Generic'
                product.save()
                updated_count += 1
        
        self.stdout.write(f'Updated {updated_count} products with brand information')
        self.stdout.write(self.style.SUCCESS('Successfully updated all products!'))
