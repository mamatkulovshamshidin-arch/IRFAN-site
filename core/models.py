from django.db import models
from django.utils.text import slugify

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: abstract = True

class Teacher(TimeStamped):
    name = models.CharField('аты-жөнү', max_length=160)
    title = models.CharField('кызматы / адистиги', max_length=180)
    biography = models.TextField('кыскача өмүр баяны')
    experience = models.CharField('тажрыйбасы', max_length=150, blank=True)
    photo = models.ImageField('сүрөт', upload_to='teachers/', blank=True)
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    class Meta: verbose_name = 'Мугалим'; verbose_name_plural = 'Мугалимдер'
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

class Category(TimeStamped):
    name = models.CharField('аталышы', max_length=100)
    description = models.TextField('түшүндүрмө')
    icon = models.CharField('иконка', max_length=40, default='book-open')
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)
    class Meta: verbose_name = 'Окуу багыты'; verbose_name_plural = 'Окуу багыттары'
    def save(self,*a,**kw):
        if not self.slug: self.slug=slugify(self.name,allow_unicode=True)
        super().save(*a,**kw)
    def __str__(self): return self.name

class Course(TimeStamped):
    title = models.CharField(max_length=160, default='Аруу жүрөк')
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    class Meta: verbose_name='Курс'; verbose_name_plural='Курстар'
    def __str__(self): return self.title

class Lesson(TimeStamped):
    title=models.CharField('сабактын аталышы',max_length=180)
    description=models.TextField('кыскача түшүндүрмө')
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='категория')
    teacher=models.ForeignKey(Teacher,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='мугалим')
    duration=models.CharField('узактыгы',max_length=60, blank=True)
    materials=models.CharField('материалдар',max_length=180,blank=True)
    status=models.CharField('статусу',max_length=80,default='Маалымат жакында жарыяланат')
    order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order','title']; verbose_name='Сабак'; verbose_name_plural='Сабактар'
    def __str__(self): return self.title

class NewsCategory(TimeStamped):
    name=models.CharField(max_length=100); slug=models.SlugField(unique=True,blank=True,allow_unicode=True)
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.name,allow_unicode=True)
        super().save(*a,**kw)
    def __str__(self):return self.name

class News(TimeStamped):
    title=models.CharField(max_length=200); excerpt=models.TextField(); content=models.TextField(); image=models.ImageField(upload_to='news/',blank=True)
    category=models.ForeignKey(NewsCategory,on_delete=models.SET_NULL,null=True,blank=True); author=models.CharField(max_length=120,blank=True)
    slug=models.SlugField(unique=True,blank=True,allow_unicode=True); published_at=models.DateField('жарыяланган күнү',auto_now_add=True)
    class Meta: ordering=['-published_at']; verbose_name='Жаңылык'; verbose_name_plural='Жаңылыктар'
    def save(self,*a,**kw):
        if not self.slug:self.slug=slugify(self.title,allow_unicode=True)
        super().save(*a,**kw)
    def __str__(self):return self.title

class Registration(TimeStamped):
    LEVELS=[('beginner','Башталгыч'),('intermediate','Орто'),('advanced','Жогорку')]
    FORMATS=[('offline','Офлайн'),('online','Онлайн'),('either','Экөө тең ылайыктуу')]
    STATUSES=[('new','Жаңы'),('contacted','Байланышылды'),('accepted','Кабыл алынды'),('declined','Баш тартты')]
    full_name=models.CharField('аты-жөнү',max_length=160); phone=models.CharField('телефон',max_length=32); email=models.EmailField(blank=True)
    age=models.PositiveSmallIntegerField('жашы'); city=models.CharField('шаары',max_length=100); education_level=models.CharField('билим деңгээли',max_length=20,choices=LEVELS)
    learning_format=models.CharField('окуу форматы',max_length=20,choices=FORMATS); notes=models.TextField('кошумча маалымат',blank=True)
    status=models.CharField(max_length=20,choices=STATUSES,default='new'); consent=models.BooleanField('маалыматтарды иштетүүгө макулдук')
    class Meta: verbose_name='Катталуу'; verbose_name_plural='Катталуулар'
    def __str__(self):return f'{self.full_name} — {self.phone}'

class Testimonial(TimeStamped):
    name=models.CharField(max_length=120); city=models.CharField(max_length=100); text=models.TextField(); photo=models.ImageField(upload_to='testimonials/',blank=True); active=models.BooleanField(default=True)
    class Meta: verbose_name='Пикир'; verbose_name_plural='Пикирлер'
    def __str__(self):return self.name

class FAQ(TimeStamped):
    question=models.CharField(max_length=240); answer=models.TextField(); category=models.CharField(max_length=100,blank=True); order=models.PositiveIntegerField(default=0)
    class Meta: ordering=['order']; verbose_name='Суроо-жооп'; verbose_name_plural='Көп берилүүчү суроолор'
    def __str__(self):return self.question

class ContactMessage(TimeStamped):
    name=models.CharField(max_length=120); email=models.EmailField(); message=models.TextField(); is_read=models.BooleanField(default=False)
    phone=models.CharField('телефон', max_length=32)
    class Meta: verbose_name='Кайрылуу'; verbose_name_plural='Кайрылуулар'
    def __str__(self):return self.name
