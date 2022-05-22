# Generated by Django 4.0.4 on 2022-05-18 15:53

from django.db import migrations


def forwards_func(apps, schema_editor):
    News = apps.get_model('mainapp', 'News')
    News.objects.create(
        title='Запуск нового курса по Python',
        preambule='Мы рады вам сообщить о запуске нового курса по Python для \
            начинающих!',
        body="... Много-много слов про Python ...",
    )
    News.objects.create(
        title='Урока по PHP в среду не состоится',
        preambule='Всем, кто не успел купить курс в понедельник, настоятельно \
            рекомендую это сделать по ссылке в конце публикации.',
        body="Сегодня в Саратове не будет проходить открытый урок по PHP, \
            который должен был состояться в среду на факультете компьютерных \
            наук СГУ. Преподавательница, за которой закреплена аудитория, \
            сказала что заболела и не придёт. На следующий урок, \
            запланированный на 28 февраля, перенесли всё, кроме курса \
            «Веб-программирование». Об этом сообщили в группе факультета в \
            социальной сети «ВКонтакте». Курс «Веб-программист» состоит из \
            двух частей. Первая — общий курс, идущий в течение 72 часов",
    )


def reverse_func(apps, schema_editor):
    News = apps.get_model('mainapp', 'News')
    News.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('mainapp', '0002_rename_courseteacher_courseteachers'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func)
    ]