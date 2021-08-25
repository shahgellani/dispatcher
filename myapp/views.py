from django.contrib.auth import authenticate
from django.db.models.functions import datetime
import logging
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Dispatches, POD
from .serializers import Employeeserializer, DispatchesSerializers

from rest_framework_swagger.views import get_swagger_view
from django.contrib.auth.models import User

schema_view = get_swagger_view(title='myapp')


class RegisterView(APIView):

    def get(self, request):
        employee = Employee.objects.all()
        serializer = Employeeserializer(employee, many=True)
        return Response(serializer.data)

    def post(self, request):
        """

        :param request:
        :return:
        """

        user = Employeeserializer(data=request.data)
        if user.is_valid():
            if User.objects.filter(username=request.data['email']):
                return Response({'Email': 'Email already exists'})
            emp = user.save()
            user = User.objects.create(username=emp.email)
            user.set_password(emp.password)
            user.save()
            token = Token.objects.get_or_create(user=user)
            return Response({'Response': "user successful created", 'token': token[1]})
        else:
            return Response({'token': 'Token couldnt be created'})


class LoginView(APIView):
    def post(self, request):
        """

        :param request:
        :return: response
        """
        email = request.data['email']
        password = request.data['password']
        user = authenticate(username=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})

        else:
            return Response({'token': 'Invalid credentials'})


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

        :param request:
        :return:
        """
        content = {'message': 'Hello, World!'}
        return Response(content)


class DispatchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        For get requests

        :return:
        """

        key = request.auth.key
        user = Token.objects.get(key=key).user

        dispatches_against_user = Dispatches.objects.filter(driver__email=user.username)
        if dispatches_against_user:
            serialized_dispatches_against_user = DispatchesSerializers(dispatches_against_user, many=True).data
            response = {'Dispatches': serialized_dispatches_against_user}

        else:
            response = {'Dispatches': 'No dispatches against this User'}

        return Response(response)

    def post(self):
        """
        For Post requests

        :return:
        """
        pass

    def put(self):
        """

        :return:
        """
        pass

    def patch(self):
        """

        :return:
        """
        pass

    def delete(self):
        """

        :return:
        """
        pass


class UpdateArrivalView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        """

        :return:
        """

        id = request.data['id']
        dispatch = Dispatches.objects.filter(id=id).first()

        dispatch.arrival_date = datetime.datetime.now()
        dispatch.save()
        return Response({'Arrival date updated'})


class UpdateDepartureView(APIView):
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        """

        :return:
        """

        id = request.data['id']
        dispatch = Dispatches.objects.filter(id=id).first()
        if dispatch.arrival_date:
            dispatch.departure_date = datetime.datetime.now()
            dispatch.status = 'Delivered'
            dispatch.save()
            response = {'Departure date updated'}
        else:
            response = {
                'Response': 'You can not update departure date before arrival date. Please first update arrival date'}

        return Response(response)


class ShowDispatchDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        """

        :param request:


        :return:
        """
        try:
            id = request.data['id']
            dispatch_detail = Dispatches.objects.filter(id=id)
            if dispatch_detail:
                logging.info("Tsting")
                serialized_data = DispatchesSerializers(dispatch_detail, many=True).data
                response = {'Dispatches Details': serialized_data}
            else:
                response = {'Response': 'No Dispatches found against this ID'}


        except:
            dispatches_detail = Dispatches.objects.all()
            if dispatches_detail:
                serialized_data = DispatchesSerializers(dispatches_detail, many=True).data
                response = {'All Dispatches': serialized_data}
            else:
                response = {'Dispatches Details': 'No details found'}
        return Response(response)


class P_O_D(APIView):
    def post(self, request):
        dispatch_id = request.data['id']

        dispatch = Dispatches.objects.filter(id=dispatch_id).first()

        try:
            image = request.data['image']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        image = POD.objects.create(image=image, dispatch=dispatch)
        image.save()
        return Response({'Response': 'Proof of delivery added'})


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
