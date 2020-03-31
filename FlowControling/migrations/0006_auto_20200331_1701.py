# Generated by Django 2.2.4 on 2020-03-31 15:01

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('FlowControling', '0005_auto_20200331_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthdata',
            name='different',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Bóle mięśni'), (2, 'Bezsenność'), (3, 'Ból głowy'), (4, 'Libido podniesione'), (5, 'Libido obniżone'), (6, 'Bolesne piersi'), (7, 'Obrzęk piersi')], max_length=13),
        ),
    ]
