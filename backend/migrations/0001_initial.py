# Initial migration of all data models to sync up with the project.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('form', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('user_type', models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher')], max_length=10)),
                ('first_name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Subtopic',
            fields=[
                ('subtopic_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('subtopic_name', models.CharField(max_length=20)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('answer_1', models.CharField(max_length=100)),
                ('answer_2', models.CharField(max_length=100)),
                ('answer_3', models.CharField(max_length=100)),
                ('answer_4', models.CharField(max_length=100)),
                ('correct_answer', models.CharField(max_length=100)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='BKT',
            fields=[
                ('bkt_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('p_initial_knowledge', models.FloatField()),
                ('p_will_learn', models.FloatField()),
                ('p_slip', models.FloatField()),
                ('p_guess', models.FloatField()),
                ('p_known', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
                ('subtopic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subtopic')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('form', models.CharField(max_length=3)),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('quiz_id', models.AutoField(primary_key=True, serialize=False)),
                ('completed', models.BooleanField(default=False)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('total_questions', models.IntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.subject')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='backend.user'),
        ),
    ]
