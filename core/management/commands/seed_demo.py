from django.core.management.base import BaseCommand
from core.models import Category, FAQ

class Command(BaseCommand):
    help = 'Нейтралдуу demo мазмунун кошот'
    def handle(self, *args, **options):
        categories = [
            ('Акыда','Ислам ишениминин негиздери.','shield-check'),
            ('Фикх','Күнүмдүк жашоодогу шарият өкүмдөрү.','scale'),
            ('Куран','Куранды окуу, түшүнүү жана ага амал кылуу.','book-open'),
            ('Хадис','Пайгамбарыбыздын ﷺ сүннөтү жана хадистери.','scroll-text'),
            ('Адеп-ахлак','Көркөм мүнөз жана инсандык тарбия.','heart'),
            ('Руханий тарбия','Жүрөктү тазалоо жана руханий өнүгүү.','sparkles'),
        ]
        for name, description, icon in categories:
            Category.objects.get_or_create(name=name, defaults={'description':description,'icon':icon})
        faqs=[
            ('Курс кимдер үчүн?','Курска диний билимди системалуу түрдө үйрөнүүнү каалагандар катыша алат.'),
            ('Окуу канча убакытка созулат?','Так график жана узактык тууралуу маалымат жакында жарыяланат.'),
            ('Курс акы төлөнөбү?','Маалымат жакында жарыяланат.'),
            ('Сабактар кайда өтөт?','Сабак өтүү жери тууралуу маалымат жакында жарыяланат.'),
            ('Онлайн окууга болобу?','Окуу форматы тууралуу маалымат жакында жарыяланат.'),
            ('Сертификат берилаби?','Маалымат жакында жарыяланат.'),
        ]
        for order,(question,answer) in enumerate(faqs): FAQ.objects.get_or_create(question=question,defaults={'answer':answer,'order':order})
        self.stdout.write(self.style.SUCCESS('Demo маалыматтары кошулду.'))
