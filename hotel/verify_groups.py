import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import Group

groups = ['Huesped', 'Gestor']
missing = []
for group_name in groups:
    if not Group.objects.filter(name=group_name).exists():
        missing.append(group_name)

if missing:
    print(f"ERROR: Missing groups: {missing}")
    exit(1)
else:
    print("SUCCESS: All required groups found.")
