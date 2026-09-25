from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from stats.selectors.stats_selector import get_platform_statistics
from stats.serializers import PlatformStatisticsSerializer


class PlatformStatisticsView(APIView):
    """
    API view returning high-level platform statistics for dashboard and landing pages.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        data = get_platform_statistics()
        serializer = PlatformStatisticsSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)
