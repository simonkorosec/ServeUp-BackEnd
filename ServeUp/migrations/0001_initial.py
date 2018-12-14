# Generated by Django 2.1.3 on 2018-12-14 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUporabnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
            ],
            options={
                'db_table': 'admin_uporabnik',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Jed',
            fields=[
                ('id_jed', models.AutoField(primary_key=True, serialize=False)),
                ('ime_jedi', models.TextField()),
                ('cena', models.FloatField()),
                ('opis_jedi', models.TextField()),
            ],
            options={
                'db_table': 'jed',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JedilniList',
            fields=[
                ('id_jedilni_list', models.AutoField(primary_key=True, serialize=False)),
                ('vrsta', models.TextField()),
            ],
            options={
                'db_table': 'jedilni_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Narocilo',
            fields=[
                ('id_narocila', models.AutoField(primary_key=True, serialize=False)),
                ('cas_prevzema', models.DateTimeField()),
                ('cas_narocila', models.DateTimeField()),
            ],
            options={
                'db_table': 'narocilo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Naslov',
            fields=[
                ('id_naslov', models.AutoField(primary_key=True, serialize=False)),
                ('ulica', models.TextField()),
                ('hisna_stevilka', models.IntegerField()),
            ],
            options={
                'db_table': 'naslov',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Posta',
            fields=[
                ('postna_stevilka', models.DecimalField(decimal_places=0, max_digits=4, primary_key=True, serialize=False)),
                ('kraj', models.TextField()),
            ],
            options={
                'db_table': 'posta',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Restavracija',
            fields=[
                ('id_restavracija', models.AutoField(primary_key=True, serialize=False)),
                ('ime_restavracije', models.TextField()),
                ('ocena', models.FloatField(blank=True, null=True)),
                ('slika', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'restavracija',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RestavracijaPodatki',
            fields=[
                ('id_restavracija', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('ime_restavracije', models.TextField(blank=True, null=True)),
                ('ocena', models.FloatField(blank=True, null=True)),
                ('tip', models.TextField(blank=True, null=True)),
                ('ulica', models.TextField(blank=True, null=True)),
                ('hisna_stevilka', models.IntegerField(blank=True, null=True)),
                ('postna_stevilka', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('kraj', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'restavracija_podatki',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TipRestavracije',
            fields=[
                ('id_tip_restavracije', models.AutoField(primary_key=True, serialize=False)),
                ('tip', models.TextField()),
            ],
            options={
                'db_table': 'tip_restavracije',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Uporabnik',
            fields=[
                ('id_uporabnik', models.TextField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'uporabnik',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='JediNarocila',
            fields=[
                ('id_jed', models.ForeignKey(db_column='id_jed', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ServeUp.Jed')),
            ],
            options={
                'db_table': 'jedi_narocila',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Nudi',
            fields=[
                ('id_restavracija', models.ForeignKey(db_column='id_restavracija', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='ServeUp.Restavracija')),
            ],
            options={
                'db_table': 'nudi',
                'managed': False,
            },
        ),
    ]
