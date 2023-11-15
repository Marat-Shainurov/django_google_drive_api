from rest_framework import serializers

from drive_api.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('name', 'data',)
