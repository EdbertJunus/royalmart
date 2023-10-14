from rest_framework import serializers, views
from rest_framework.response import Response

from .serializers import UploadExcelSerializer

class UploadExcelView(views.APIView):

    def post(self, request):
        serializer = UploadExcelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the uploaded file.
        excel_file = serializer.validated_data['sales_file']
        print(serializer)
        # print(excel_file)
        # serializer.save()
        return Response('Excel file uploaded and processed successfully.')