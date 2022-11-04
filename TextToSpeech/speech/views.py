from rest_framework.views import APIView
from rest_framework.response import Response
from main import edge_print_read
from . models import Image

class ManageSpeechView(APIView):
    def post(self, request, format=None):

        try:
            data = request.data
            print("data:", data)
        except:
            return Response(
                {"error": "input image"}
            )

        try:
            image = data['image']
            print("image:", image)
        except:
            return Response(
                {"error": "cannot retrieve image"}
            )

        try:
            Image.objects.create(
                image_url = image
            )

            latest_id = Image.objects.all().values_list('id', flat=True).order_by('-id').first()
            print("latest_id:", latest_id)
            filter_img = Image.objects.get(id=latest_id)
            print("filter_img:", filter_img)
            image_path = filter_img.image_url.path
            print("image_path_views:", image_path)

            edge_print_read(image_path)
        except:
            return Response(
                {"error": "Something went wrong!"}
            )
        return Response(
            {"Done": "finsihsed executing"}
        )