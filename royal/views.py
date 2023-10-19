from rest_framework import serializers, views
from rest_framework.response import Response
import os
import pandas as pd
from django.core.files.storage import FileSystemStorage
from .serializers import UploadExcelSerializer
from .models import SalesDetail
from .utils import handleSalesFile

class UploadExcelView(views.APIView):

    def post(self, request):
        serializer = UploadExcelSerializer(data=request.data)
        if serializer.is_valid():
            salesFile = request.FILES['fileSales']
            excelData = pd.read_excel(salesFile)
            salesData = handleSalesFile(excelData)
            periode = serializer.validated_data.get('periode')
            for dbframe in salesData.itertuples():
                obj = SalesDetail.objects.create(salesId=periode, 
                namaProduk=dbframe._2, kode=dbframe.KODE, 
                qty=dbframe.QTY, jumlah=dbframe.JUMLAH, 
                hargaPokok=dbframe._6)

                obj.save()
            serializer.validated_data['fileSales'] = None
        serializer.save()
        return Response('Excel file uploaded and processed successfully.')