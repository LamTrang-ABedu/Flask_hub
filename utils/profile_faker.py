from faker import Faker
import random

def generate_profile(locale='en_US'):
    fake = Faker(locale)
    gender = random.choice(['male', 'female'])
    first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
    last_name = fake.last_name()
    full_name = f"{first_name} {last_name}"
    parent_last_name = last_name
    father_first = fake.first_name_male()
    return {
        'first_name': first_name,
        'last_name': last_name,
        'name': full_name,
        'gender': gender,
        'dob': fake.date_of_birth(minimum_age=18, maximum_age=50).isoformat(),
        'email': fake.email(),
        'cell_phone': fake.phone_number(),
        'phone': fake.phone_number(),
        'ssn': fake.ssn() if hasattr(fake, 'ssn') else 'N/A',
        'street': fake.street_address(),
        'city': fake.city(),
        'country': fake.current_country() if hasattr(fake, 'current_country') else 'N/A',
        'zip_code': fake.postcode(),
        'parent': {
            'first_name': father_first,
            'last_name': parent_last_name,
            'email': fake.email()
        }
    }
