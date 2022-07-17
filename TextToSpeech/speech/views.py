from rest_framework.views import APIView
from rest_framework.response import Response
from main import edge_print_read
import os

class ManageSpeechView(APIView):
    def post(self, request, format=None):
        data = request.data
        try:
            image = data['image']
            print("image:", image)
        except:
            return Response(
                {"error": "Enter an image"}
            )
        try:
            foo = os.path.abspath("image")
            edge_print_read(foo)
        except:
            return Response(
                {"error": "Something went wrong!"}
            )
        return Response(
            {"success": "Okay boss"}
        )