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
from .tasks import send_email_task

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from shops_online.settings import LOGGER_NAME


response_schema = openapi.Response(
    description='Описание ответа',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    )
	)
	


class OrganizationListView(APIView):
	http_method_names = ['get']
	permission_classes = [IsAuthenticated]
	authentication_classes = [JWTAuthentication]
	@swagger_auto_schema(
    responses={
        200: response_schema
    },
	security=[{"Bearer": []}],
	)
	def get (self, request):
		try:
			organizations = Organization.objects.all()
			serializer = OrganizationSerializer(organizations, many=True)
			# логирование
			LOGGER_NAME.info('GET запрос был выполнен успешно')
			return Response(serializer.data, status=status.HTTP_200_OK)
		except Exception as e:
			LOGGER_NAME.info(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
class ShopView(APIView):
	response_schema = openapi.Response(
    description='Описание ответа',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    )
	)
	@swagger_auto_schema(
    responses={
        200: response_schema
    },
	)
	@permission_classes([IsAuthenticated])
	@background(schedule=10)
	def put (request, id):
		try:
			shop = Shop.objects.get(id=id)
			serializer_shop = ShopSerializer(shop, data=request.data)
			if serializer_shop.is_valid():
				serializer_shop.save()

				email = 'dvolkov@yandex.ru'
				subject = 'Subject of the email'
				message = 'Message body of the email'
				
				send_email_task(email, subject, message)
				
				LOGGER_NAME.info('PUT запрос был выполнен успешно')
				return Response(serializer_shop.data)
			else:
				return Response(serializer_shop.errors, status=status.HTTP_400_BAD_REQUEST)
		except Shop.DoesNotExist:
			LOGGER_NAME.info(f'Магазин с id={id} не найден')
			return Response(f'Магазин с id={id} не найден', status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			LOGGER_NAME.info(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
class shops_file(APIView):
	response_schema = openapi.Response(
    description='Описание ответа',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    )
	)
	@swagger_auto_schema(
    responses={
        200: response_schema
    },
	)
	@permission_classes([IsAuthenticated])
	def shops_file(request, id):
		try:
			organization = Organization.objects.get(id=id)
			shops_csv = organization.shop_set.all()
			data_shops = [{'id': shop.id, 'name': shop.name} for shop in shops_csv]
			df = pd.DataFrame(data_shops, columns=["id", "name"])
			filename = f"shops_{'organization_id'}.xlsx"
			df.to_excel(filename, index=False)
			LOGGER_NAME.info('Запрос был выполнен успешно')
			return Response(open(filename, 'rb'), as_attachment=True)
		except Organization.DoesNotExist:
			LOGGER_NAME.info(f'Организация с id={id} не найдена')
			return Response(f'Организация с id={id} не найдена', status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			LOGGER_NAME.info(f'Произошла ошибка при выполнении запроса: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

