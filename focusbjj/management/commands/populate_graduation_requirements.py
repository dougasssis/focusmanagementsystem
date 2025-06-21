from django.core.management.base import BaseCommand
from focusbjj.models import GraduationRequirement
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates the graduation requirements table with default values'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating graduation requirements table...')
        
        with transaction.atomic():
            # First, delete existing requirements
            count = GraduationRequirement.objects.count()
            if count > 0:
                self.stdout.write(f'Deleting {count} existing requirements...')
                GraduationRequirement.objects.all().delete()
            
            # Belt and stripe requirements organized by progression
            belts = [
                'White',
                'Gray/White', 
                'Gray', 
                'Gray/Black',
                'Yellow/White', 
                'Yellow', 
                'Yellow/Black',
                'Orange/White', 
                'Orange', 
                'Orange/Black',
                'Green/White', 
                'Green', 
                'Green/Black',
                'Blue',
                'Purple',
                'Brown',
                'Black'
            ]
            
            stripes = ['No Stripes', 'Iº Stripe', 'IIº Stripe', 'IIIº Stripe', 'IVº Stripe']
            
            # Set requirements based on belt type
            requirements = {
                # White to Blue Belt path (adults)
                'White': 25, # First stripe at 25 classes
                
                # Kids belts all at 30 classes per stripe
                'Gray/White': 30,
                'Gray': 30,
                'Gray/Black': 30,
                'Yellow/White': 30,
                'Yellow': 30,
                'Yellow/Black': 30,
                'Orange/White': 30,
                'Orange': 30,
                'Orange/Black': 30,
                'Green/White': 30,
                'Green': 30,
                'Green/Black': 30,
                
                # Colored belts for adults
                'Blue': 50,
                'Purple': 60,
                'Brown': 65
            }
            
            # White Belt progression - last stripe needs more classes
            for i, stripe in enumerate(stripes):
                if i == 0:
                    # Skip White Belt with No Stripes
                    continue
                elif i == 4:  # IVº Stripe (last one)
                    GraduationRequirement.objects.create(
                        belt='White', stripes=stripe, required_classes=40
                    )
                elif i >= 2:  # IIº and IIIº Stripes
                    GraduationRequirement.objects.create(
                        belt='White', stripes=stripe, required_classes=30
                    )
                else:  # Iº Stripe
                    GraduationRequirement.objects.create(
                        belt='White', stripes=stripe, required_classes=25
                    )
            
            # Create requirements for all other belts
            for belt in belts[1:]:  # Skip White Belt which was already handled
                if belt == 'Black':
                    # Black belt only needs one entry - no stripes
                    GraduationRequirement.objects.create(
                        belt=belt, stripes='No Stripes', required_classes=0
                    )
                else:
                    # Create entries for each stripe
                    for stripe in stripes:
                        GraduationRequirement.objects.create(
                            belt=belt, stripes=stripe, required_classes=requirements.get(belt, 30)
                        )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully created {GraduationRequirement.objects.count()} graduation requirements')) 