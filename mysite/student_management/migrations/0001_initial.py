# Generated by Django 4.1.13 on 2024-06-24 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('School_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=100)),
                ('Address', models.TextField(max_length=100)),
                ('City', models.CharField(max_length=20)),
                ('Phone_No', models.CharField(max_length=10)),
                ('Postal_Code', models.CharField(max_length=6)),
                ('Fax_No', models.CharField(max_length=10)),
                ('Email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('User_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=50)),
                ('Phone_No', models.IntegerField(max_length=10)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('Role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('Student_Id', models.AutoField(primary_key=True, serialize=False)),
                ('First_Name', models.CharField(max_length=20)),
                ('Last_Name', models.CharField(max_length=20)),
                ('Gender', models.CharField(max_length=10)),
                ('Email', models.EmailField(max_length=254, unique=True)),
                ('Standard', models.CharField(max_length=5)),
                ('DOB', models.DateField()),
                ('Address', models.TextField(max_length=200)),
                ('City', models.CharField(max_length=100)),
                ('Phone_No', models.CharField(max_length=10)),
                ('Parents_Phone_No', models.CharField(max_length=10)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management.school')),
            ],
        ),
    ]
