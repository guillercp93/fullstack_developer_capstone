"""
Populate Database with Sample Data

This module populates the database with sample car make and model data.
It creates car makes and adds a few models for each make.
"""

from .models import CarMake, CarModel


def initiate():
    car_make_data = [
        {
            "name": "Toyota",
            "description": "Japanese multinational automotive manufacturer known for reliability and quality",
            "logo_url": "https://www.toyota.com/assets/img/common/logo.png",
            "website": "https://www.toyota.com",
            "founded_year": 1937,
        },
        {
            "name": "Honda",
            "description": "Japanese manufacturer known for cars, motorcycles and power equipment",
            "logo_url": "https://www.honda.com/images/logo.png",
            "website": "https://www.honda.com",
            "founded_year": 1948,
        },
        {
            "name": "Ford",
            "description": "American multinational automaker and pioneer of the modern automotive industry",
            "logo_url": "https://www.ford.com/assets/ford/logo.png",
            "website": "https://www.ford.com",
            "founded_year": 1903,
        },
        {
            "name": "BMW",
            "description": "German luxury vehicle and motorcycle manufacturer known for performance",
            "logo_url": "https://www.bmw.com/assets/img/logo.png",
            "website": "https://www.bmw.com",
            "founded_year": 1916,
        },
        {
            "name": "Tesla",
            "description": "American electric vehicle and clean energy company",
            "logo_url": "https://www.tesla.com/assets/img/logo.png",
            "website": "https://www.tesla.com",
            "founded_year": 2003,
        },
    ]

    # Create car makes
    for make_data in car_make_data:
        make, created = CarMake.objects.get_or_create(
            name=make_data["name"],
            defaults={
                "description": make_data["description"],
                "logo_url": make_data["logo_url"],
                "website": make_data["website"],
                "founded_year": make_data["founded_year"],
            },
        )

        # Add some models for each make
        if created:
            if make.name == "Toyota":
                models = [
                    {"name": "Camry", "type_car": "SEDAN", "year": 2023},
                    {"name": "RAV4", "type_car": "SUV", "year": 2023},
                    {"name": "Corolla", "type_car": "SEDAN", "year": 2022},
                ]
            elif make.name == "Honda":
                models = [
                    {"name": "Civic", "type_car": "SEDAN", "year": 2023},
                    {"name": "CR-V", "type_car": "SUV", "year": 2023},
                    {"name": "Accord", "type_car": "SEDAN", "year": 2022},
                ]
            elif make.name == "Ford":
                models = [
                    {"name": "F-150", "type_car": "SUV", "year": 2023},
                    {"name": "Mustang", "type_car": "SEDAN", "year": 2023},
                    {"name": "Explorer", "type_car": "SUV", "year": 2022},
                ]
            elif make.name == "BMW":
                models = [
                    {"name": "3 Series", "type_car": "SEDAN", "year": 2023},
                    {"name": "X5", "type_car": "SUV", "year": 2023},
                    {"name": "5 Series", "type_car": "SEDAN", "year": 2022},
                ]
            elif make.name == "Tesla":
                models = [
                    {"name": "Model 3", "type_car": "SEDAN", "year": 2023},
                    {"name": "Model Y", "type_car": "SUV", "year": 2023},
                    {"name": "Model S", "type_car": "SEDAN", "year": 2022},
                ]

            # Create car models for this make
            for model_data in models:
                CarModel.objects.create(
                    maker=make,
                    name=model_data["name"],
                    type_car=model_data["type_car"],
                    year=model_data["year"],
                )
