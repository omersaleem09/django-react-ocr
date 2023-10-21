# Generated by Django 4.2.6 on 2023-10-19 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_remove_extractedtext_extracted_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extractedtext',
            old_name='e_address',
            new_name='emp_last_name',
        ),
        migrations.RenameField(
            model_name='extractedtext',
            old_name='e_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='extractedtext',
            name='emp_address',
        ),
        migrations.RemoveField(
            model_name='extractedtext',
            name='obm_no',
        ),
    ]