# Generated by Django 5.0.2 on 2024-11-27 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_creditcard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='card_holder_name',
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='card_number',
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='cvv',
        ),
        migrations.RemoveField(
            model_name='creditcard',
            name='expiration_date',
        ),
        migrations.AddField(
            model_name='creditcard',
            name='card_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Enter the card amount.', max_digits=10),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='card_photo',
            field=models.ImageField(blank=True, help_text='Upload a clear photo of the card.', null=True, upload_to='card_photos/'),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='card_pin',
            field=models.CharField(help_text='Enter the car subscription number.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='creditcard',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
