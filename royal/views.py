from rest_framework import serializers, views, viewsets, status
from rest_framework.response import Response
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .serializers import SalesSerializer, UserSerializer, StockSerializer, StockUploadSerializer, MasterSerializer
from .models import SalesDetail, Sales, Stock
from .utils import handleSalesFile, handleMasterFile, sort_by_date, handleMasterSupplier
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
import datetime, json

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
            
            salesDetailObject = [
                SalesDetail(salesId=periode, 
                namaProduk=dbframe._2, kode=dbframe.KODE, 
                qty=dbframe.QTY, jumlah=dbframe.JUMLAH, 
                hargaPokok=dbframe._6)
                for dbframe in salesData.itertuples()
            ]
            # for dbframe in salesData.itertuples():
            #     obj = SalesDetail.objects.create(salesId=periode, 
            #     namaProduk=dbframe._2, kode=dbframe.KODE, 
            #     qty=dbframe.QTY, jumlah=dbframe.JUMLAH, 
            #     hargaPokok=dbframe._6)

            #     obj.save()
            SalesDetail.objects.bulk_create(salesDetailObject)
            serializer.validated_data['fileSales'] = None
        serializer.save()
        return JsonResponse({'message':'Excel file uploaded and processed successfully.'}, status=status.HTTP_200_OK)  

    def get(self, request):

        sales = [sales.periode for sales in Sales.objects.all()]
        sorted_month = sorted(sales, key=sort_by_date)

        return JsonResponse({'data':sorted_month}, status=status.HTTP_200_OK)       

class RegisterView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

class StockView(views.APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StockUploadSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            stockFile = request.FILES['stockFile']
            df = pd.read_excel(stockFile)
            clean_df = handleMasterSupplier(df)
            stocks = [
                Stock(kode=dbframe.KODE, 
                namaProduk=dbframe._2, bs=dbframe.BS, total=dbframe.TOTAL, supplier=dbframe.Supplier)
                for dbframe in clean_df.itertuples()
            ]
            if Stock.objects.all().exists():
                Stock.objects.all().delete()
            Stock.objects.bulk_create(stocks)
            return JsonResponse({'message': 'success'}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        stocks = [{'kode': stock.kode, 'namaProduk' : stock.namaProduk, 'bs' : stock.bs, 'total' : stock.total} for stock in Stock.objects.all()]
        return JsonResponse({'data':stocks}, status=status.HTTP_200_OK)

class MasterView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MasterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            periode = serializer.validated_data.get('periode')
            periode = periode.split(',')
            stock_queryset = Stock.objects.all().values_list('kode', 'namaProduk', 'bs', 'total', 'supplier')
            stock_df = pd.DataFrame(list(stock_queryset), columns=['kode', 'namaProduk', 'bs', 'total', 'supplier'])
            salesMonth = list(Sales.objects.all().values_list('periode'))
            salesMonth = [month[0] for month in salesMonth]

            chosenMonth = []
            for m in periode:
                if(m in salesMonth):
                    chosenMonth.append(m)
            
            sorted_month = sorted(chosenMonth, key=sort_by_date)
            print(sorted_month)
            for i, periode in enumerate(sorted_month):
                month = periode.split(' ')[0][:3]
                year = periode.split(' ')[1][-2:]
                sales_queryset = SalesDetail.objects.filter(salesId=periode).values_list('namaProduk', 'kode', 'qty')
                
                sales_df = pd.DataFrame(list(sales_queryset), columns=['namaProduk', 'kode', 'qty'])
                sales_df['qty'] = sales_df['qty'].astype('Int64')
                
                stock_df = stock_df.merge(sales_df[['kode', 'qty']], how='left', on='kode', suffixes=[None, '_'+ str(month+'_'+year)])
                
            initial_month = sorted_month[0].split(' ')[0][:3]
            initial_year = sorted_month[0].split(' ')[1][-2:]
            stock_df.rename(columns={ 'qty' : 'qty_'+str(initial_month)+"_"+str(initial_year)}, inplace=True)
            result = stock_df.to_dict(orient="records")
            jsonResult = json.dumps(result)
            return JsonResponse({'result': jsonResult}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)

class UserView(views.APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        username= str(request.user.username)
        return JsonResponse({'username': username}, status=status.HTTP_200_OK)