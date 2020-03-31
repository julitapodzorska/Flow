# Generated by Django 2.2.4 on 2020-03-31 09:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('FlowControling', '0003_auto_20200331_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthdata',
            name='different',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'ból piersi'), (2, 'Obrzęk piersi'), (3, 'Bóle mięśni'), (4, 'Bezsenność'), (5, 'Ból głowy'), (6, 'Libido podniesione'), (7, 'Libido obniżone')], max_length=13),
        ),
    ]