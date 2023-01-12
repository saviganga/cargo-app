from rest_framework import serializers
from cargo import models as cargo_models

class CargoInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = cargo_models.CargoInfo
        fields = "__all__"

class CargoByNameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    confidence_value = serializers.IntegerField(required=True)