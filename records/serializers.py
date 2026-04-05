from rest_framework import serializers
from .models import FinancialRecord, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type']

class FinancialRecordSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = FinancialRecord
        fields = ['id', 'amount', 'type', 'category', 'category_name',
                  'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value