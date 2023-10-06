from rest_framework import serializers
from .models import Organization, Shop


# Create your views here.
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'index']



class OrganizationSerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = ['name', 'description', 'shops']