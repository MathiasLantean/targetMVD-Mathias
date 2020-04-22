# Generated by Django 3.0.3 on 2020-04-22 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('target', '0005_target_topic'),
        ('contact', '0002_initial_contact_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_one', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_one_set', to='target.Target')),
                ('target_two', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_two_set', to='target.Target')),
            ],
        ),
        migrations.AddConstraint(
            model_name='chat',
            constraint=models.UniqueConstraint(fields=('target_one', 'target_two'), name='unique_chat_between_targets_one_two'),
        ),
        migrations.AddConstraint(
            model_name='chat',
            constraint=models.UniqueConstraint(fields=('target_two', 'target_one'), name='unique_chat_between_targets_two_one'),
        ),
    ]
