from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer
from .models import Shop
from .serializers import ShopSerializer
from django.http import HttpResponse

# 3 task
import csv
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from rest_framework.decorators import api_view
import pandas as pd

# Создание метода GET /api/organizations/

class OrganizationListView(APIView):
	def get (self, request):
		organizations = Organization.objects.filter(is_deleted=False)
		serializer = OrganizationSerializer
		return Response(serializer.data)

# Создание метода PUT /api/shops/{id}/

class ShopView(APIView):
	def put (self, request, id):
		try:
			shop = Shop.objects.get(pk=id)
		except Shop.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		serializer_shop = ShopSerializer(shop, data=request.data)
		if serializer.is_valid():
			serializer_shop.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Создание метода GET /organizations/{id}/shops_file/ который будет возвращать файл с расширением xlsx или csv

class download_shops_file(APIView):
	def get_shops_file(request, id):
		organization = Organization.objects.get(id=id)
		shops_csv = organization.shop_set.all()
		data_shops = [
		{'id': [shop.id for shop in shops_csv], 'name': [shop.name for shop in shops_csv]}
	    ]
	    df = pd.DataFrame(data_shops, columns=["id", "name"])
	    filename = f"shops_{organization_id}.xlsx"
	    df.to_excel(filename, index=False)
	    return filename

