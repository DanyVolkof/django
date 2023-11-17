from django.shortcuts import render
from rest_framework.views import APIView
from .models import Shop, Organization
from shop.serializers import OrganizationSerializer, ShopSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import logging
from django.http import HttpResponse
#10 task
from django.core.mail import send_mail
from background_task import background
from background_task.models import Task

from background_task.models import Task
from .tasks import send_email_task

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView



class OrganizationListView(APIView):
	def get (self, request):
		try:
			organizations = Organization.objects.filter(is_deleted=False)
			serializer = OrganizationSerializer(organizations, many=True)
			self.authentication_classes = [JWTAuthentication()]
			# логирование
			logging.info('GET запрос был выполнен успешно')
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			logging.error(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
class ShopView(APIView):
	def put (self, request, id):
		try:
			shop = Shop.objects.get(id=id)
			serializer_shop = ShopSerializer(shop, data=request.data)
			if serializer_shop.is_valid():
				serializer_shop.save()
				
				# Создание и запуск фоновой задачи
				@background(schedule=10)
				def send_email_background_task(recipient, subject, message):
					send_email_task(email, subject, message)

				email = 'dvolkov@yandex.ru'
				subject = 'Subject of the email'
				message = 'Message body of the email'
				
				send_email_background_task(email, subject, message)
				
				logging.info('PUT запрос был выполнен успешно')
				return Response(serializer_shop.data)
			else:
				return Response(serializer_shop.errors, status=status.HTTP_400_BAD_REQUEST)
		except Shop.DoesNotExist:
			logging.error(f'Магазин с id={id} не найден')
			return Response(f'Магазин с id={id} не найден', status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			logging.error(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
class shops_file(APIView):
	def shops_file(self, request, id):
		try:
			organization = Organization.objects.get(id=id)
			shops_csv = organization.shop_set.all()
			data_shops = [{'id': shop.id, 'name': shop.name} for shop in shops_csv]
			df = pd.DataFrame(data_shops, columns=["id", "name"])
			filename = f"shops_{'organization_id'}.xlsx"
			df.to_excel(filename, index=False)
			logging.info('Запрос был выполнен успешно')
			return Response(open(filename, 'rb'), as_attachment=True)
		except Organization.DoesNotExist:
			logging.error(f'Организация с id={id} не найдена')
			return Response(f'Организация с id={id} не найдена', status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			logging.error(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



