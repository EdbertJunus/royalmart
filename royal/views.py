from rest_framework import serializers, views, viewsets, status
from rest_framework.response import Response
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .serializers import SalesSerializer, UserSerializer, StockSerializer, StockUploadSerializer
from .models import SalesDetail, Sales, Stock
from .utils import handleSalesFile, handleMasterFile
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated

class SalesView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            salesFile = request.FILES['fileSales']
            periode = serializer.validated_data.get('periode')
            if Sales.objects.filter(periode=periode).exists():
                Sales.objects.filter(periode=periode).delete()
                SalesDetail.objects.filter(salesId=periode).delete()
            excelData = pd.read_excel(salesFile)
            salesData = handleSalesFile(excelData)
            
            for dbframe in salesData.itertuples():
                obj = SalesDetail.objects.create(salesId=periode, 
                namaProduk=dbframe._2, kode=dbframe.KODE, 
                qty=dbframe.QTY, jumlah=dbframe.JUMLAH, 
                hargaPokok=dbframe._6)

                obj.save()
            serializer.validated_data['fileSales'] = None
        serializer.save()
        return JsonResponse({'message':'Excel file uploaded and processed successfully.'}, status=status.HTTP_200_OK)  

    def get(self, request):

        sales = [sales.periode for sales in Sales.objects.all()]
        return JsonResponse({'data':sales}, status=status.HTTP_200_OK)       

class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

class StockView(views.APIView):
    
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StockUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            stockFile = request.FILES['stockFile']
            df = pd.read_excel(stockFile)
            clean_df = handleMasterFile(df)
            stocks = [
                Stock(kode=dbframe.KODE, 
                namaProduk=dbframe._2, bs=dbframe.BS, total=dbframe.TOTAL)
                for dbframe in clean_df.itertuples()
            ]
            print(Stock.objects.all().exists())
            if Stock.objects.all().exists():
                Stock.objects.all().delete()
            Stock.objects.bulk_create(stocks)
            return JsonResponse({'message': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)