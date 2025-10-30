from rest_framework import generics
from .serializers import UserRegistrationSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from .serializers import UserRegistrationSerializer
#
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
