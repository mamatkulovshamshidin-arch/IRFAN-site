from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from .forms import ContactForm, RegistrationForm
from .models import Category, FAQ, Lesson, News, Teacher, Testimonial

def home(request):
    return render(request, 'core/home.html', {'categories':Category.objects.all()[:6], 'lessons':Lesson.objects.all()[:5], 'teachers':Teacher.objects.all()[:3], 'news':News.objects.all()[:3], 'faqs':FAQ.objects.all()[:5], 'testimonials':Testimonial.objects.filter(active=True)[:3]})
def about(request): return render(request,'core/about.html')
def program(request): return render(request,'core/program.html',{'lessons':Lesson.objects.select_related('category','teacher')})
def teachers(request): return render(request,'core/teachers.html',{'teachers':Teacher.objects.all()})
def teacher_detail(request, slug):
    return render(request, 'core/teacher_detail.html', {'teacher': get_object_or_404(Teacher, slug=slug)})
def faq(request): return render(request, 'core/faq.html', {'faqs': FAQ.objects.all()})
def news_list(request):
    query=request.GET.get('q',''); items=News.objects.select_related('category')
    if query: items=items.filter(Q(title__icontains=query)|Q(excerpt__icontains=query))
    return render(request,'core/news_list.html',{'page_obj':Paginator(items,6).get_page(request.GET.get('page')),'query':query})
def news_detail(request,slug): return render(request,'core/news_detail.html',{'article':get_object_or_404(News,slug=slug), 'related':News.objects.exclude(slug=slug)[:3]})
def register(request):
    form=RegistrationForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        form.save(); messages.success(request,'Катталуу арызыңыз кабыл алынды. Биз сиз менен байланышабыз.'); return redirect('registration_success')
    return render(request,'core/register.html',{'form':form})
def registration_success(request): return render(request,'core/success.html')
def contact(request):
    form=ContactForm(request.POST or None)
    if request.method=='POST' and form.is_valid(): form.save(); messages.success(request,'Кайрылууңуз жөнөтүлдү. Рахмат!'); return redirect('contact')
    return render(request,'core/contact.html',{'form':form})
def error_404(request,exception): return render(request,'errors/404.html',status=404)
def error_403(request,exception): return render(request,'errors/403.html',status=403)
def error_500(request): return render(request,'errors/500.html',status=500)
def robots(request):
    return HttpResponse('User-agent: *\nAllow: /\nSitemap: ' + request.build_absolute_uri(reverse('sitemap')) + '\n', content_type='text/plain')
def sitemap(request):
    paths=['home','about','program','teachers','news','register','contact']
    urls=''.join(f'<url><loc>{request.build_absolute_uri(reverse(name))}</loc></url>' for name in paths)
    urls+=''.join(f'<url><loc>{request.build_absolute_uri(reverse("news_detail",args=[item.slug]))}</loc></url>' for item in News.objects.all())
    return HttpResponse(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',content_type='application/xml')
