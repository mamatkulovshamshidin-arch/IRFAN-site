from rest_framework import serializers, viewsets, permissions, filters
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample
from .models import Category, FAQ, Lesson, News, Teacher


# ─────────────────────────────────────────────
# Serializers
# ─────────────────────────────────────────────

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'icon')
        read_only_fields = ('id', 'slug')


class TeacherSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True, allow_null=True, required=False)

    class Meta:
        model = Teacher
        fields = ('id', 'name', 'slug', 'title', 'biography', 'experience', 'photo')
        read_only_fields = ('id', 'slug')


class LessonSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    teacher = TeacherSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Lesson
        fields = (
            'id', 'title', 'description',
            'category', 'category_id',
            'teacher', 'teacher_id',
            'duration', 'materials', 'status', 'order',
        )
        read_only_fields = ('id',)


class NewsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'slug', 'category', 'excerpt', 'content', 'image', 'author', 'published_at')
        read_only_fields = ('id', 'slug', 'published_at')


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('id', 'question', 'answer', 'category', 'order')
        read_only_fields = ('id',)


# ─────────────────────────────────────────────
# Permission helper
# ─────────────────────────────────────────────

def _permissions(request, obj=None):
    """GET — всем. POST/PUT/PATCH/DELETE — только admin."""
    if request.method in permissions.SAFE_METHODS:
        return True
    return request.user and request.user.is_staff


class ReadOrAdmin(permissions.BasePermission):
    """GET open, write operations require is_staff."""
    def has_permission(self, request, view):
        return _permissions(request)

    def has_object_permission(self, request, view, obj):
        return _permissions(request, obj)


# ─────────────────────────────────────────────
# ViewSets — Category
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Окуу багыттарынын тизмеси',
        description='Бардык окуу багыттарын кайтарат. Аутентификация талап кылынбайт.',
    ),
    retrieve=extend_schema(
        summary='Бир окуу багытынын маалыматы',
        description='ID боюнча бир окуу багытын кайтарат.',
    ),
    create=extend_schema(
        summary='Жаңы окуу багыты түзүү',
        description='**Admin гана.** Жаңы окуу багытын түзөт.',
    ),
    update=extend_schema(
        summary='Окуу багытын толук жаңыртуу (PUT)',
        description='**Admin гана.** Окуу багытын толук жаңыртат.',
    ),
    partial_update=extend_schema(
        summary='Окуу багытын жарым-жартылай жаңыртуу (PATCH)',
        description='**Admin гана.** Окуу багытынын айрым талааларын жаңыртат.',
    ),
    destroy=extend_schema(
        summary='Окуу багытын жок кылуу (DELETE)',
        description='**Admin гана.** Окуу багытын өчүрөт.',
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOrAdmin]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['id']


# ─────────────────────────────────────────────
# ViewSets — Teacher
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Мугалимдердин тизмеси',
        description='Бардык мугалимдерди кайтарат.',
    ),
    retrieve=extend_schema(
        summary='Бир мугалимдин маалыматы',
        description='Slug боюнча бир мугалимди кайтарат.',
    ),
    create=extend_schema(
        summary='Жаңы мугалим кошуу',
        description='**Admin гана.** Жаңы мугалим жазуусун түзөт.',
    ),
    update=extend_schema(
        summary='Мугалимди толук жаңыртуу (PUT)',
        description='**Admin гана.**',
    ),
    partial_update=extend_schema(
        summary='Мугалимди жарым-жартылай жаңыртуу (PATCH)',
        description='**Admin гана.**',
    ),
    destroy=extend_schema(
        summary='Мугалимди жок кылуу (DELETE)',
        description='**Admin гана.**',
    ),
)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [ReadOrAdmin]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'title', 'biography']
    ordering_fields = ['name', 'id']
    ordering = ['id']


# ─────────────────────────────────────────────
# ViewSets — Lesson
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Сабактардын тизмеси',
        description='Бардык сабактарды тартип боюнча кайтарат.',
    ),
    retrieve=extend_schema(
        summary='Бир сабактын маалыматы',
        description='ID боюнча бир сабакты кайтарат.',
    ),
    create=extend_schema(
        summary='Жаңы сабак түзүү',
        description='**Admin гана.** `category_id` жана `teacher_id` менен байланышты орнотуңуз.',
    ),
    update=extend_schema(
        summary='Сабакты толук жаңыртуу (PUT)',
        description='**Admin гана.**',
    ),
    partial_update=extend_schema(
        summary='Сабакты жарым-жартылай жаңыртуу (PATCH)',
        description='**Admin гана.**',
    ),
    destroy=extend_schema(
        summary='Сабакты жок кылуу (DELETE)',
        description='**Admin гана.**',
    ),
)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('category', 'teacher').all()
    serializer_class = LessonSerializer
    permission_classes = [ReadOrAdmin]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title', 'id']
    ordering = ['order', 'title']


# ─────────────────────────────────────────────
# ViewSets — News
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Жаңылыктардын тизмеси',
        description='Бардык жаңылыктарды жарыяланган күнү боюнча кайтарат.',
    ),
    retrieve=extend_schema(
        summary='Бир жаңылыктын толук маалыматы',
        description='Slug боюнча бир жаңылыкты кайтарат.',
    ),
    create=extend_schema(
        summary='Жаңы жаңылык жазуу',
        description='**Admin гана.**',
    ),
    update=extend_schema(
        summary='Жаңылыкты толук жаңыртуу (PUT)',
        description='**Admin гана.**',
    ),
    partial_update=extend_schema(
        summary='Жаңылыкты жарым-жартылай жаңыртуу (PATCH)',
        description='**Admin гана.**',
    ),
    destroy=extend_schema(
        summary='Жаңылыкты жок кылуу (DELETE)',
        description='**Admin гана.**',
    ),
)
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.select_related('category').all()
    serializer_class = NewsSerializer
    permission_classes = [ReadOrAdmin]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'title']
    ordering = ['-published_at']


# ─────────────────────────────────────────────
# ViewSets — FAQ
# ─────────────────────────────────────────────

@extend_schema_view(
    list=extend_schema(
        summary='Көп берилүүчү суроолордун тизмеси',
        description='Бардык FAQ жазууларын кайтарат.',
    ),
    retrieve=extend_schema(
        summary='Бир FAQ жазуусунун маалыматы',
        description='ID боюнча бир FAQ жазуусун кайтарат.',
    ),
    create=extend_schema(
        summary='Жаңы FAQ суроо-жооп кошуу',
        description='**Admin гана.**',
    ),
    update=extend_schema(
        summary='FAQ жазуусун толук жаңыртуу (PUT)',
        description='**Admin гана.**',
    ),
    partial_update=extend_schema(
        summary='FAQ жазуусун жарым-жартылай жаңыртуу (PATCH)',
        description='**Admin гана.**',
    ),
    destroy=extend_schema(
        summary='FAQ жазуусун жок кылуу (DELETE)',
        description='**Admin гана.**',
    ),
)
class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [ReadOrAdmin]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['question', 'answer', 'category']
    ordering_fields = ['order', 'id']
    ordering = ['order']
