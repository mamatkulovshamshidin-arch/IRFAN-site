from django.contrib import admin
from .models import Category, ContactMessage, Course, FAQ, Lesson, News, NewsCategory, Registration, Teacher, Testimonial

admin.site.site_header = 'ИРФАН башкаруу панели'
admin.site.site_title = 'ИРФАН Admin'
admin.site.index_title = 'Курсту жана сайтты башкарыңыз'
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display=('full_name','phone','city','status','created_at'); list_filter=('status','education_level','learning_format'); search_fields=('full_name','phone','email'); list_editable=('status',)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display=('title','category','published_at'); list_filter=('category',); search_fields=('title','excerpt'); prepopulated_fields={'slug':('title',)}
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=('name','title','experience'); search_fields=('name','title'); prepopulated_fields={'slug':('name',)}
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=('title','category','teacher','status','order'); list_filter=('category','status'); list_editable=('order',)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}
@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin): prepopulated_fields={'slug':('name',)}
admin.site.register([Course, Testimonial, FAQ, ContactMessage])
