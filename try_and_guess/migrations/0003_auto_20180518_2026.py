# Generated by Django 2.0.1 on 2018-05-18 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('try_and_guess', '0002_auto_20180518_1721'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameStatus',
        ),
        migrations.AlterField(
            model_name='game',
            name='guesser',
            field=models.CharField(choices=[('USER', 'USER'), ('MACHINE', 'MACHINE')], default='USER', max_length=15),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.CharField(choices=[('START', 'START'), ('USER_GUESSING', 'USER_GUESSING'), ('MACHINE_GUESSING', 'MACHINE_GUESSING'), ('FINISHED', 'FINISHED')], default='START', max_length=25),
        ),
    ]
