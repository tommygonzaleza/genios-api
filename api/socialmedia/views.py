from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        # Check if the request has the file part
        if 'file' not in request.FILES:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        # Validate file type; ensure it's a CSV
        if not file.name.endswith('.csv'):
            return Response({"error": "File format not supported. Please upload a CSV file."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Further validation can be done via MIME type, which is a bit more secure
        if file.content_type != 'text/csv':
            return Response({"error": "Invalid file type. Only CSV files are accepted."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Reading the CSV file
            data = pd.read_csv(file)
            # Optionally, process the data here

            # Returning some information about the file for now
            return Response({"message": "File has been uploaded and read successfully!", "data": data.head().to_dict()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
