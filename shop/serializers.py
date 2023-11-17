from rest_framework import serializers
from shop.models import Organization, Shop
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['name', 'description', 'address', 'index']



class OrganizationSerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True, read_only=True)
    class Meta:
        model = Organization
        fields = ['name', 'description', 'shops']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token