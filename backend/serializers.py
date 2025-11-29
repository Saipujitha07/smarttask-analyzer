from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.DateField(required=False)
    estimated_hours = serializers.FloatField(required=False, default=1)
    importance = serializers.IntegerField(required=False, default=5)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False)
