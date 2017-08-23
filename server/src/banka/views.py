from rest_framework.response import Response
from rest_framework.views import APIView

from banka.utils import get_balance


class BankaAPIView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        data = {
            'balance': get_balance(),
        }
        return Response(data)
