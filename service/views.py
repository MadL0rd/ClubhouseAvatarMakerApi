from rest_framework import viewsets, mixins
from service.serializers import BorderSerializer, NewBorderSerializer, CodeSerializer, SettingJsonSerializer
from service.models import Border, Code, SettingJson
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import status
import datetime
from django.db.models import Q


class AllowAnonymous(BasePermission):

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class SettingJsonViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = SettingJsonSerializer
    queryset = SettingJson.objects.all().order_by('pk')


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BorderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BorderSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Border.objects.exclude(brand__isnull=False).order_by('pk')

    def get_queryset(self):
        q = self.request.GET.get('query')
        qs = self.queryset
        if q:
            qs = qs.filter(title__istartswith=q).order_by('pk')
        return qs


class GetToken(APIView):
    permission_classes = [AllowAnonymous]
    # отправляет код для авторизации

    @staticmethod
    def get(request):
        count_users = User.objects.all().count()
        username = count_users+1
        user = User.objects.create_user(
            username=username,
            password=User.objects.make_random_password()
        )
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class CodesViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer
    queryset = Code.objects.all().order_by('pk')

    def create(self, request, *args, **kwargs):
        user = request.user
        errs = []
        data = request.data
        now = datetime.datetime.now().date()
        code = Code.objects.filter(name=data.get('code')).first()
        if code is not None:
            if code in user.codes.all():
                errs.append('Вы уже используете этот промокод')
            if code.start_date is not None and now < code.start_date:
                errs.append('Код ещё не введён в оборот')
            elif code.end_date is not None and now > code.end_date:
                errs.append('Код закончил своё действие')
            if code.available_users_count <= 0:
                errs.append('Количество людей, доступных для использования промокода закончилось')
        else:
            errs.append('Такого промокода не существует')
        if errs:
            return Response({'errors': errs}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.codes.add(code)
            return Response({}, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        return user.codes.all().order_by('pk')


class BrandViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NewBorderSerializer
    queryset = Border.objects.all().order_by('pk')

    def list(self, request, *args, **kwargs):
        user = request.user
        codes = list(user.codes.all().values_list('id', flat=True))
        queryset = Border.objects.filter(brand__isnull=False).filter(Q(code__in=codes) | Q(code__isnull=True)).order_by('pk')
        serializer = self.get_serializer(queryset, many=True)
        pre_data = serializer.data
        new_data = {}
        for border in pre_data:
            brand = border['brand']
            if new_data.get(brand) is None:
                new_data[brand] = [border]
            else:
                new_data[brand].append(border)
        resp = []
        for k, v in new_data.items():
            resp.append({
                "brand": k,
                "borders": v,
            })
        return Response(resp)
