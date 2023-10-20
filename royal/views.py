from rest_framework import serializers, views, viewsets, status
from rest_framework.response import Response
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .serializers import SalesSerializer
from .models import SalesDetail, Sales
from .utils import handleSalesFile
from django.http.response import JsonResponse

class SalesView(views.APIView):

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
        return Response('Excel file uploaded and processed successfully.')

    def get(self, request):

        sales = [sales.periode for sales in Sales.objects.all()]
        return JsonResponse({'data':sales}, status=status.HTTP_200_OK)       
