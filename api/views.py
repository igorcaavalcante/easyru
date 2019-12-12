from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from core.models import Consumer, Transaction, Gru, User
from core.serializers import ConsumerSerializer, TransactionSerializer, GruSerializer, UserSerializer

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_me(request):
    try:
        user = User.objects.get(username=request.user.username)
    except Consumer.DoesNotExist:
        return HttpResponse(status=404)

    if user.is_consumer:
        try:
            consumer = Consumer.objects.get(user__username=user.username)
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
    else:
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data)

        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE':
            user.delete()
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

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def gru(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = GruSerializer(data=data)
        if serializer.is_valid():
            serializer.create(validated_data=data)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'GET':
        try:
            gru_list = Gru.objects.filter(consumer_cpf=request.user.username)
        except Gru.DoesNotExist:
            return HttpResponse(status=404)

        serializer = GruSerializer(gru_list, many=True)
        return JsonResponse(serializer.data, safe=False)
