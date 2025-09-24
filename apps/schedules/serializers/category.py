from rest_framework import serializers
from apps.schedules.models import ScheduleCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCategory
        fields = ['id', 'name', 'color', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_color(self, value):
        if value and (not value.startswith('#') or len(value) != 7):
            raise serializers.ValidationError("Color must be a valid hex code (e.g., #RRGGBB).")
        return value