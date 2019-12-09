from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from core.models import Consumer, Transaction
from core.serializers import ConsumerSerializer, TransactionSerializer

@csrf_exempt
def consumer(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConsumerSerializer(data=data)
        if serializer.is_valid():
            serializer.create(validated_data=data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def consumer_views(request):
    try:
        consumer = Consumer.objects.get(user__username=request.user.username)
    except Consumer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ConsumerSerializer(consumer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ConsumerSerializer(consumer, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        consumer.delete()
        return HttpResponse(status=204)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction(request):
    try:
        transaction_list = Transaction.objects.filter(consumer_cpf=request.user.username)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction_list, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def transaction_views(request, id):
    try:
        transaction = Transaction.objects.get(id=id)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)
