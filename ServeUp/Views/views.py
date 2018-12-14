from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from url_filter.integrations.drf import \
    DjangoFilterBackend  # https://github.com/miki725/django-url-filter - how to use filters

from ServeUp.serializers import *


def get_restaurants(location):
    """
    Helper method that return a list of restaurants in the specified location
    :param location: name of the city
    :return: list of restaurants
    """
    posta = Posta.objects.get(kraj__contains=location)
    data = RestavracijaPodatki.objects.filter(postna_stevilka=posta.postna_stevilka)
    return RestavracijaPodatkiSerializer(data, many=True).data


class RestavracijaPodatkiViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    queryset = RestavracijaPodatki.objects.all()
    serializer_class = RestavracijaPodatkiSerializer


class RestavracijaViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    queryset = Restavracija.objects.all()
    serializer_class = RestavracijaSerializer

    @action(detail=False, methods=['POST'])
    def home(self, request):
        response = {}

        try:
            location = request.data['location']
        except Exception:
            location = None

        if location is None:
            response['status'] = 0
            response['description'] = "Error: Please input the location"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response['status'] = 1
            response['description'] = "Restaurants for city: " + location + "."
            response['data'] = get_restaurants(location)
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        The function receives a JSON data with the admin email, restaurant name,
        restaurant type, address and rating
        Return values
        status: 0 - Error, 1 - OK
        description: Short description of Error or confirm desired action
        additional actions: Set of actions that also had to be performed, in ex. updating address table
        """
        response = {'status': "",
                    'description': "",
                    'additional actions': ""}

        # Get admin id
        id_admin = AdminUporabnik.objects.get(email=request.data['email']).id

        # Deal with address id
        requested_data = request.data['naslov'].split(', ')
        address = requested_data[0].split(' ')
        post = requested_data[1].split(' ')

        try:
            id_address = Naslov.objects.get(ulica=" ".join(address[:-1]), hisna_stevilka=address[-1]).id_naslov
        except Naslov.DoesNotExist:
            naslov_data = {'ulica': " ".join(address[:-1]),
                           'hisna_stevilka': address[-1],
                           'postna_stevilka': post[0]}

            # Add post to Posta table, if it doesn't exist
            try:
                query_posta = Posta.objects.get(postna_stevilka=post[0])
            except Posta.DoesNotExist:
                posta_data = {'postna_stevilka': post[0], 'kraj': post[1]}
                serializer_posta = PostaSerializer(data=posta_data)
                if serializer_posta.is_valid():
                    serializer_posta.save()
                    response['additional actions'] += "\nUpdated Posta table"
                else:
                    response['status'] = 0
                    response['description'] = serializer_posta.errors
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

            # Add address to Naslov table, if it doesn't exist
            serializer_naslov = NaslovSerializer(data=naslov_data)
            if serializer_naslov.is_valid():
                serializer_naslov.save()
                response['additional actions'] += "\nUpdated Address table"
            else:
                response['status'] = 0
                response['description'] = serializer_naslov.errors
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            id_address = Naslov.objects.get(ulica=" ".join(address[:-1]), hisna_stevilka=address[-1]).id_naslov

        # Build JSON object
        data = {'id_admin': id_admin,
                'ime_restavracije': request.data['ime_restavracije'],
                'id_tip_restavracije': request.data['id_tip_restavracije'],
                'id_naslov': id_address, 'ocena': request.data['ocena']}

        serializer = RestavracijaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['status'] = 1
            response['description'] = "Restaurant added to admin"
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response['status'] = 0
            response['description'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PostaViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['postna_stevilka', 'kraj']

    serializer_class = PostaSerializer
    queryset = Posta.objects.all()
    model = Posta


class TipRestavracijeViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    serializer_class = TipRestavracijeSerializer
    queryset = TipRestavracije.objects.all()
    model = TipRestavracije


class AdminUporabnikViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AdminUporabnikSerializer
    queryset = AdminUporabnik.objects.all()
    model = AdminUporabnik

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
        The function receives JSON data with the email and the password. If the user exist and the password is
        correct we return the id of the restaurant the user manages, if he does not manage any restaurant returns None.
        Return values
        status: 0 - Error, 1 - OK
        description: Short description of Error or confirm desired action
        id_restavracija: If status 1, id of restaurant or None
        """
        response = {}

        # First try to get the user
        try:
            user = AdminUporabnik.objects.get(email=request.data['email'])
        except AdminUporabnik.DoesNotExist:
            user = None

        # if user exist check password
        if user is not None:
            password = request.data['password']
            match = check_password(password, user.password)
            if not match:
                response['status'] = 0
                response['description'] = "Password does not match"
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
            else:
                query = Restavracija.objects.all().filter(id_admin=user.id)
                data = RestavracijaSerializer(query, many=True).data
                if len(data) != 0:
                    id_restavracija = data[0]['id_restavracija']
                else:
                    id_restavracija = None
                response['status'] = 1
                response['description'] = "Username and password match"
                response['id_restavracija'] = id_restavracija
                return Response(response, status=status.HTTP_200_OK)
        else:
            response['status'] = 0
            response['description'] = "Username does not exist"
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        The function receives JSON data with the email and the password.
        If the input data is valid it creates a new admin user.
        Return values
        status: 0 - Error, 1 - OK
        description: Short description of Error or confirm desired action
        """
        serializer = AdminUporabnikSerializer(data=request.data)
        response = {}
        if serializer.is_valid():
            serializer.save()
            response['status'] = 1
            response['description'] = "New user created"
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            email_error = ("Email - " + serializer.errors['email'][
                0]) if 'email' in serializer.errors else ""
            password_error = (
                    "Password - " + serializer.errors['password'][
                0]) if 'password' in serializer.errors else ""

            response['status'] = 0
            response['description'] = "Error: " + email_error + password_error
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UporabnikViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UporabnikSerializer
    queryset = Uporabnik.objects.all()
    model = Uporabnik

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """
        The function receives JSON data with the token of the new user.
        If the input data is valid it creates a new user.
        Return values
        status: 0 - Error, 1 - New user created, 2 - User already registered
        description: Short description of Error or confirm desired action
        """
        try:
            user = Uporabnik.objects.get(id_uporabnik=request.data['id_uporabnik'])
        except Uporabnik.DoesNotExist:
            user = None

        response = {}
        if user is None:
            serializer = UporabnikSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response['status'] = 1
                response['description'] = "New user created"
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                id_error = "ID: " + serializer.errors['id_uporabnik'][0]
                response['status'] = 0
                response['description'] = "Error: " + id_error
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response['status'] = 2
            response['description'] = "User already registered"
            return Response(response, status=status.HTTP_200_OK)
