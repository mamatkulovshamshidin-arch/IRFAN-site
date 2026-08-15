from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('core', '0001_initial')]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='phone',
            field=models.CharField(max_length=32, verbose_name='телефон'),
        ),
    ]
