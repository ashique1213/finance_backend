from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import FinancialRecord, Category
from .serializers import FinancialRecordSerializer, CategorySerializer
from core.permissions import IsAdminUser, IsAnalystOrAdmin, IsViewerOrHigher

class FinancialRecordListCreateView(APIView):
    permission_classes = [IsViewerOrHigher]   # Viewer can list, Analyst/Admin can create

    def get(self, request):
        records = FinancialRecord.objects.filter(user=request.user)
        serializer = FinancialRecordSerializer(records, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.role not in ['analyst', 'admin']:
            return Response({"error": "You do not have permission to create records"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = FinancialRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinancialRecordDetailView(APIView):
    permission_classes = [IsViewerOrHigher]

    def get_object(self, pk):
        try:
            return FinancialRecord.objects.get(pk=pk, user=self.request.user)
        except FinancialRecord.DoesNotExist:
            return None

    def get(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = FinancialRecordSerializer(record)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.role not in ['analyst', 'admin']:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object(pk)
        if not record:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FinancialRecordSerializer(record, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != 'admin':
            return Response({"error": "Only Admin can delete records"}, status=status.HTTP_403_FORBIDDEN)
        record = self.get_object(pk)
        if not record:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        record.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)