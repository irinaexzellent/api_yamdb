from django.shortcuts import get_object_or_404
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets,status,permissions
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from reviews.models import Category, Comments, Genre, Review, Title, User
from .pagination import CategoryGenrePagination
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          AuthSerializer, RoleforReadSerializer,
                          ObtainTokenSerializer, UserSerializer)
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .permissions import IsAdminOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Titles, id=title_id)
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        get_object_or_404(Titles, id=title_id)    
        serializer.save(author=self.request.user,
                        title_id=title_id)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, id=review_id)   
        new_queryset = Comments.objects.filter(review_id=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        get_object_or_404(Review, id=review_id)    
        serializer.save(author=self.request.user,
                        title_id=review_id)


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        # if self.action == 'create':
        # return (AdminostratorOnly(),)
        return super().get_permissions()


class CategoryDelete(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    #permission_classes = (AdminOnly,)


class GenreListCreate(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

    def get_permissions(self):
        # if self.action == 'create':
        # return (AdminostratorOnly(),)
        return super().get_permissions()


class GenreDelete(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    #permission_classes = (AdminOnly,)


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name')
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'),)


class TitleList(generics.ListCreateAPIView):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = CategoryGenrePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class TitleViewSet(generics.RetrieveDestroyAPIView):
    serializer_class = TitleSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('pk')
        return Title.objects.filter(pk=title_id)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    permission_classes = (
        IsAuthenticated,
        IsAdminOnly,
    )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_account_information(self, request):
        serializer = UserSerializer(self.request.user)
        if request.method == 'PATCH':
            user = self.request.user
            serializer = RoleforReadSerializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APISignUp(APIView):
    """Регистрация нового пользователя."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user = serializer.save()
        mail_subject = 'Ваш код подтверждения'
        message = f'Код подтверждения - {user.confirmation_code}'

        send_mail(
            mail_subject,
            message,
            settings.EMAIL_FROM,
            (email, )
        )

        if serializer.validated_data['username'] == 'me':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    """Получение токена"""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (
          serializer.validated_data['confirmation_code']
          == user.confirmation_code
        ):
            token = RefreshToken.for_user(request.user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
