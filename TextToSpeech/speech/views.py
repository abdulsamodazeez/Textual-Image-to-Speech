from rest_framework.views import APIView
from rest_framework.response import Response
from main import edge_print_read
from . models import Image
from rest_framework import status
from main import *

class ManageSpeechView(APIView):
    def post(self, request, format=None):

        try:
            data = request.data
        except:
            return Response(
                {"error": "input image"},
            )

        try:
            image = data['image']
        except:
            return Response(
                {"error": "cannot retrieve image"}
            )

        try:
            Image.objects.create(
                image_url = image
            )

            latest_id = Image.objects.all().values_list('id', flat=True).order_by('-id').first()
            filter_img = Image.objects.get(id=latest_id)
            image_path = filter_img.image_url.path
            text = edge_print_read(image_path)
        except:
            return Response(
                {"error": "Something went wrong!"}
            )
        
        try:
            latest_id = Image.objects.all().values_list('id', flat=True).order_by('-id').first()
            filter_img = Image.objects.get(id=latest_id)
            filter_img.delete()
        except:
            return Response(
                {"error": "Couldn't delete img!"}
            )

        return Response(
            {"text": text},
            status=status.HTTP_200_OK
        )