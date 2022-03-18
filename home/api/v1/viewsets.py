from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from home.api.v1.serializers import (
    SignupSerializer, AppSerializer, PlanSerializer,
    UserSerializer, SubscriptionSerializer
)
from home.models import (
    App,
    Plan,
    Subscription
)


class AppViewSet(ModelViewSet):
    serializer_class = AppSerializer
    queryset = App.objects.all()


class PlanViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()


class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})
