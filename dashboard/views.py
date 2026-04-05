from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from records.models import FinancialRecord
from core.permissions import IsViewerOrHigher

class DashboardSummaryView(APIView):
    permission_classes = [IsViewerOrHigher]

    def get(self, request):
        records = FinancialRecord.objects.filter(user=request.user)

        total_income = records.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = records.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0

        return Response({
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_balance": float(total_income - total_expense),
            "total_records": records.count(),
        })