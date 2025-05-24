from django.core.management.base import BaseCommand
from chatbot.models import Rule
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Import data from Excel files into the Rule model'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--type', type=str, choices=['vehicle', 'product'], required=True,
                          help='Type of data being imported (vehicle or product)')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        data_type = options['type']

        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f'File not found: {excel_file}'))
            return

        try:
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            rules_created = 0
            if data_type == 'vehicle':
                # Process vehicle data
                for _, row in df.iterrows():
                    # Create pattern from make and model
                    pattern = f"What are the tire specifications for {row['MAKE']} {row['MODEL']} {row['CYEAR']}?"
                    
                    # Create detailed response
                    response = f"Tire specifications for {row['MAKE']} {row['MODEL']} {row['CYEAR']}:\n"
                    response += f"Tire Size: {row['TIRESIZE']}\n"
                    response += f"Load Index: {row['LOADINDEX']}\n"
                    response += f"Speed Rating: {row['SPEEDRATE']}\n"
                    response += f"Ply: {row['PLY']}\n"
                    response += f"Section Width: {row['SECWIDTH']}\n"
                    response += f"Aspect Ratio: {row['ASPRATIO']}\n"
                    response += f"Rim Size: {row['RIM']}\n"
                    response += f"Run Flat: {row['RUNFLAT']}\n"
                    response += f"TPMS: {row['TPMS']}\n"
                    response += f"Vehicle Type: {row['VEHTYPE']}\n"
                    response += f"Front Inflation: {row['FRONTINF']}\n"
                    response += f"Rear Inflation: {row['REARINF']}\n"
                    response += f"Fuel Type: {row['VEH_ENGINE_FUEL_TYPE']}"

                    Rule.objects.get_or_create(
                        pattern=pattern,
                        response=response
                    )
                    rules_created += 1

            elif data_type == 'product':
                # Process product data
                for _, row in df.iterrows():
                    # Create pattern from description
                    pattern = f"Tell me about {row['DESC']}"
                    
                    # Create detailed response
                    response = f"Product Information for {row['DESC']}:\n"
                    response += f"Size: {row['DisplaySize']}\n"
                    response += f"Generic Size: {row['Generic_Size']}\n"
                    response += f"Tire Size: {row['Tire_Size']}\n"
                    response += f"Speed Rating: {row['Web_Displayed_Speed_Rating']}\n"
                    response += f"Load Index: {row['Load_Index']}\n"
                    response += f"Load Range: {row['Load_Range']}\n"
                    response += f"Plys: {row['Plys']}\n"
                    response += f"Tread Type: {row['Tread_Type']}\n"
                    response += f"Sidewall Style: {row['Sidewall_Style']}\n"
                    response += f"Model Name: {row['Model_Name']}\n"
                    response += f"Performance Categories: {row['PerformanceCategories1']}, {row['PerformanceCategories2']}\n"
                    response += f"Price: ${row['TirePrice']}\n"
                    response += f"Installation Cost: ${row['Installation_Cost']}"

                    Rule.objects.get_or_create(
                        pattern=pattern,
                        response=response
                    )
                    rules_created += 1

            self.stdout.write(self.style.SUCCESS(f'Successfully imported {rules_created} rules from {excel_file}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}')) 