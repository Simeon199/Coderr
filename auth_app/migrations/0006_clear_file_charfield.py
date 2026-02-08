from django.db import migrations, models


def clear_empty_file_values(apps, schema_editor):
    """Set empty string file values to NULL before FK migration."""
    CustomUser = apps.get_model('auth_app', 'CustomUser')
    CustomUser.objects.filter(file='').update(file=None)


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_alter_customuser_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='file',
            field=models.CharField(max_length=100, null=True, blank=True, default=None),
        ),
        migrations.RunPython(clear_empty_file_values, migrations.RunPython.noop),
    ]
