from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.schedules.models import Schedule

class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'title', 'description', 'start_datetime', 'end_datetime',
                   'is_all_day' , 'category', 'status' , 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        start_datetime = data.get('start_datetime')
        end_datetime = data.get('end_datetime')

        if start_datetime and end_datetime:
            if end_datetime < start_datetime:
                raise serializers.ValidationError("End datetime must be after start datetime.")
        return data
