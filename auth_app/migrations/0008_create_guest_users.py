import binascii
import os

from django.contrib.auth.hashers import make_password
from django.db import migrations


GUEST_USERS = [
    {
        'username': 'andrey',
        'password': 'asdasd',
        'type': 'customer',
    },
    {
        'username': 'kevin',
        'password': 'asdasd24',
        'type': 'business',
    },
]


def create_guest_users(apps, schema_editor):
    """
    Ensure the two guest users (customer + business) required by the
    frontend's guest login exist, each with a matching profile and auth
    token. Idempotent: safe to run on fresh and existing databases.
    """
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    CustomerProfile = apps.get_model('profile_app', 'CustomerProfile')
    BusinessProfile = apps.get_model('profile_app', 'BusinessProfile')
    Token = apps.get_model('authtoken', 'Token')

    for guest in GUEST_USERS:
        user, created = CustomUser.objects.get_or_create(
            username=guest['username'],
            defaults={
                'type': guest['type'],
                'password': make_password(guest['password']),
            },
        )

        if guest['type'] == 'customer':
            CustomerProfile.objects.get_or_create(user=user)
        else:
            BusinessProfile.objects.get_or_create(user=user)

        Token.objects.get_or_create(
            user=user,
            defaults={'key': binascii.hexlify(os.urandom(20)).decode()},
        )


def remove_guest_users(apps, schema_editor):
    """
    Reverse operation: remove the guest users (cascades to their
    profiles and tokens via the existing FK relations).
    """
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    CustomUser.objects.filter(
        username__in=[g['username'] for g in GUEST_USERS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0007_alter_customuser_file'),
        ('profile_app', '0008_remove_businessprofile_file_and_more'),
        ('authtoken', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_guest_users, remove_guest_users),
    ]
