from django.shortcuts import render
import logging

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

#10 task
from django.core.mail import send_mail
from background_task import background
from background_task.models import Task

logger = logging.getLogger('Shop')

# Создание метода GET /api/organizations/

class OrganizationListView(APIView):
	def get (self, request):
		try:
			organizations = Organization.objects.filter(is_deleted=False)
			serializer = OrganizationSerializer
			# логирование
			logger.info('GET запрос был выполнен успешно')
			return Response(serializer.data), HttpResponse('GET запрос выполнен успешно')
		except Exception as e:
			logger.error(f'Произошла ошибка при выполнении GET запроса: {e}')
			return HttpResponseServerError('Произошла ошибка при выполнении GET запроса')


# Отправка письма на email
@background(schedule=5)
def send_email_task(email, subject, message):
	send_mail(
		subject=subject,
        message=message,
        from_email='your_email@example.com',
        recipient_list=[email],
        fail_silently=True,
    )



# Создание метода PUT /api/shops/{id}/

class ShopView(APIView):
	def put (self, request, id):
		try:
			shop = Shop.objects.get(pk=id)
			# логирование
			logger.info('GET запрос был выполнен успешно')
			return HttpResponse('GET запрос выполнен успешно')
		except Shop.DoesNotExist:
			logger.error(f'Произошла ошибка при выполнении GET запроса: {e}')
			return Response(status=status.HTTP_404_NOT_FOUND)
		    # отправка письма
		tasks = Task.objects.filter(task_name='Shop.views.send_email_task', task_params=f'["{email}", "{subject}", "{message}"]')
		if tasks.exists():
			tasks.delete()
		send_email_task(request.data['email'], request.data['subject'], request.data['message'])

		serializer_shop = ShopSerializer(shop, data=request.data)
		if serializer.is_valid():
			serializer_shop.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        


# Создание метода GET /organizations/{id}/shops_file/ который будет возвращать файл с расширением xlsx или csv

class download_shops_file(APIView):
	def get_shops_file(request, id):
		try:
			organization = Organization.objects.get(id=id)
			shops_csv = organization.shop_set.all()
			data_shops = [
			{'id': [shop.id for shop in shops_csv], 'name': [shop.name for shop in shops_csv]}
			]
			df = pd.DataFrame(data_shops, columns=["id", "name"])
			filename = f"shops_{organization_id}.xlsx"
			df.to_excel(filename, index=False)
			logger.info('Запрос был выполнен успешно')
			return filename, HttpResponse('Запрос выполнен успешно')
		except Exception as e:
        logger.error(f'Произошла ошибка при выполнении запроса: {e}')
        return HttpResponseServerError('Произошла ошибка при выполнении запроса')

