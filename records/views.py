from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FinancialRecord, Category
from .serializers import FinancialRecordSerializer, CategorySerializer
from core.permissions import IsAdminUser, IsAnalystOrAdmin, IsViewerOrHigher

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class FinancialRecordViewSet(viewsets.ModelViewSet):
    serializer_class = FinancialRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'category', 'date']
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return FinancialRecord.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsViewerOrHigher()]
        elif self.action in ['create', 'update', 'partial_update']:
            return [IsAnalystOrAdmin()]
        elif self.action == 'destroy':
            return [IsAdminUser()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)