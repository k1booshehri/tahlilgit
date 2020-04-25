from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, RegisterSerializer2, UserSerializer2, OfficeSerializer, UserSerializer3, RateSerializer, RateUpdateSerializer
from .models import office, User


# showing offices


class OfficeViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = office.objects.filter(doctor=request.user)
        serializer = OfficeSerializer(queryset, many=True)
        return Response(serializer.data)


# filtering doctors list
class DoctorsViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer3

    def get_queryset(self):
        return User.objects.filter(edu=self.kwargs['edu'])

# office api


class OfficeAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = OfficeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        off = serializer.save()
        return Response({
            "office": OfficeSerializer(off, context=self.get_serializer_context()).data
        })


# Register api


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data, "token": AuthToken.objects.create(user)[1]
        })


class RegisterAPI2(generics.GenericAPIView):
    serializer_class = RegisterSerializer2

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer2(user, context=self.get_serializer_context()).data, "token": AuthToken.objects.create(user)[1]
        })

# login api


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data, "token": AuthToken.objects.create(user)[1]
        })


# get user api


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserAPI2(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer2

    def get_object(self):
        return self.request.user


class OfficesViewset(viewsets.ModelViewSet):

    queryset = office.objects.all()
    serializer_class = OfficeSerializer

    def get_queryset(self):
        return office.objects.filter(doctor=self.kwargs['id'])


class RateSetAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = RateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        off = serializer.save()
        perializer = RateUpdateSerializer(data=request.data)
        perializer.is_valid(raise_exception=True)
        on = perializer.save()
        return Response({
            "Rate": RateSerializer(off, context=self.get_serializer_context()).data
        })
