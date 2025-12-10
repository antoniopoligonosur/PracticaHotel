import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import Group

groups = ['Huesped', 'Gestor']
for group_name in groups:
    group, created = Group.objects.get_or_create(name=group_name)
    if created:
        print(f"Group '{group_name}' created.")
    else:
        print(f"Group '{group_name}' already exists.")
