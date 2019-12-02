from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models import Consumer, Transaction
from core.serializers import ConsumerSerializer, TransactionSerializer

@csrf_exempt
def consumer(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConsumerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def consumer_views(request, consumer_cpf):
    try:
        consumer = Consumer.objects.get(cpf=consumer_cpf)
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
def transaction(request, id):
    try:
        transaction = Transaction.objects.get(id=id)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

@csrf_exempt
def transaction_views(request, consumer_cpf):
    try:
        transaction_list = Transaction.objects.filter(consumer_cpf=consumer_cpf)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction_list, many=True)
        return JsonResponse(serializer.data, safe=False)
