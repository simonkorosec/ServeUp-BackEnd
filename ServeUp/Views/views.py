from django.contrib.auth.hashers import check_password
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json
from django.forms.models import model_to_dict
from django.db.models import ObjectDoesNotExist

from ServeUp.Views.helper import *


class NarociloViewSet(viewsets.ModelViewSet):
    """
    ViewSet provides 'list', 'create', 'retrieve', 'update' and 'destroy' actions

    Additional actions can be added using '@action()' decorator, default response
    is GET, you can add POST using 'methods' argument
    """
    queryset = Narocilo.objects.all()
    serializer_class = NarociloSerializer

    def list(self, request, *args, **kwargs):
        """
        Returns all orders for restaurant with specified id in GET parameter 'id_restavracija'.

        ORDER_NEW = 0  # "Nova Naročila"
        ORDER_PREPARING = 1  # "V Pripravi"
        ORDER_DONE = 2  # "Pripravljeno"
        ORDER_FINISHED = 3  # "Končano"
        """
        get_params = request.query_params
        response = {}
        return_data = {}

        try:
            id_restavracija = get_params['id_restavracija']
        except KeyError:
            response['status'] = 0
            response['description'] = "Missing id, add ?id_restavracija=x to call"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        data = JediNarocilaPodatki.objects.filter(id_restavracija=id_restavracija,
                                                  status__in=[ORDER_NEW, ORDER_DONE, ORDER_PREPARING, ORDER_FINISHED])
        data = JediNarocilaPodatkiSerializer(data, many=True).data

        for order in data:
            id_narocila = order['id_narocila']
            if id_narocila not in return_data:
                return_data[id_narocila] = {
                    'cas_prevzema': order['cas_prevzema'],
                    'cas_narocila': order['cas_narocila'],
                    'id_restavracija': order['id_restavracija'],
                    'id_uporabnik': order['id_uporabnik'],
                    'cena': 0,
                    'id_narocila': order['id_narocila'],
                    'status': order['status'],
                    'checked_in': order['checked_in'],
                    'id_miza': order['id_miza'],
                    'jedi': []
                }

            return_data[id_narocila]['jedi'].append({
                'id_jed': order['id_jed'],
                'ime_jedi': order['ime_jedi'],
                'kolicina': order['kolicina'],
                'cena': order['cena']
            })
            return_data[id_narocila]['cena'] += order['cena']

        response['status'] = 1
        response['data'] = list(return_data.values())
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def refresh(self, request):
        """
        Returns new and cancelled orders for a restaurant
        GET params:
        id_restavracija: id of the restaurant to refresh orders
        """
        get_params = request.query_params
        response = {}

        try:
            id_restavracija = get_params['id_restavracija']
        except KeyError:
            response['status'] = 0
            response['description'] = "Missing id, add ?id_restavracija=x to call"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        new, cancelled, checked_in = get_new_cancelled_checked_in_orders(int(id_restavracija))
        response['status'] = 1
        response['new_orders'] = new
        response['cancelled_orders'] = cancelled
        response['checked_in_orders'] = checked_in
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def cancel_order(self, request):
        """
        Receive order id and delete that order from the database effectively cancelling it.
        Add the order id to the cancelled orders list
        Return conformation of action or error.
        """
        response = {}
        data = json.load(request)
        try:
            order_id = data['id_narocilo']
        except KeyError as e:
            response['status'] = 0
            response['description'] = "Missing key data " + str(e) + ""
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # noinspection PyBroadException
        try:
            narocilo = Narocilo.objects.get(id_narocila=order_id)
            order = {'id_narocila': narocilo.id_narocila, 'id_restavracija': narocilo.id_restavracija.id_restavracija}
            narocilo.delete()
            add_cancelled_order(order)
            response['status'] = 1
            response['description'] = "Successfully deleted order"
            return Response(response, status=status.HTTP_200_OK)
        except Exception:
            response['status'] = 0
            response['description'] = "Could not delete order {}".format(order_id)
            return Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    @action(detail=False, methods=['POST'])
    def new_order(self, request):
        """
        The function receives JSON data with the details of a new order and stores it.
        Return values
        status: 0 - Error, 1 - Successfully added
        description: Short description of Error or confirm desired action
        """
        response = {}
        data = json.load(request)

        try:
            order = {
                "cas_prevzema": data['cas_prevzema'],
                "cas_narocila": data['cas_narocila'],
                "id_restavracija": data['id_restavracija'],
                "id_uporabnik": data['id_uporabnik'],
                "status": ORDER_NEW,
                "checked_in": False
            }
            meals = data['jedi']
        except KeyError as e:
            response['status'] = 0
            response['description'] = "Missing key data " + str(e) + ""
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if len(meals) == 0:  # If there are no meals in order wrong formatting
            response['status'] = 0
            response['description'] = "No meal data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = NarociloSerializer(data=order)
        if serializer.is_valid():
            narocilo = serializer.save()
            id_narocila = narocilo.id_narocila

            success, price = add_meals_to_order(meals, id_narocila)
            if not success:  # Something went wrong delete order
                narocilo.delete()
                response['status'] = 0
                response['description'] = "Could not insert meals"
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            order['cena'] = price
            order['id_narocila'] = id_narocila
            order['jedi'] = meals
            add_new_order(order)
            response['status'] = 1
            response['description'] = "New order created"
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response['status'] = 0
            response['description'] = "Could not add new order"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def status_update(self, request):
        response = {'status': "",
                    'description': ""}
        order = Narocilo.objects.get(id_narocila=request.data['id_narocilo'])
        data = model_to_dict(order)
        data["status"] = request.data["status"]

        if not 0 <= request.data["status"] <= 3:
            response['status'] = 0
            response['description'] = "Invalid status value"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        serializer = NarociloSerializer(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            response['status'] = 1
            response['description'] = "Successfully changed status"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['status'] = 0
            response['description'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
        """
        The function receives JSON data with the name of a city.
        Return all restaurants in given city.
        Return values
        status: 0 - Error
        description: Short description of Error or confirm desired action

        If valid input return only array of restaurants, request by Urban.
        """
        response = {}
        try:
            location = request.data['location']
        except KeyError:
            location = None

        if location is None:
            response['status'] = 0
            response['description'] = "Error: Please input the location"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = get_restaurants(location)
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
                Posta.objects.get(postna_stevilka=post[0])
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

    @action(detail=False, methods=['GET'])
    def fetch_qr(self, request):
        """
        Function receives id_restavracija parameter
        Returns all QR codes for a given id_restavracija
        Return values:
            status: 0 || 1
            data: JSON array with QR codes
        """

        get_params = request.query_params
        response = {}
        return_data = []

        try:
            id_restavracija = get_params['id_restavracija']
        except KeyError:
            response['status'] = 0
            response['description'] = "Missing id, add ?id_restavracija=x to call"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        data = Mize.objects.filter(id_restavracija=id_restavracija)
        data = MizeSerializer(data, many=True).data

        for obj in data:
            id_miza = obj['id_miza']
            if id_miza not in return_data:
                return_data.append(id_miza)

        response['status'] = 1
        response['data'] = return_data
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def add_table(self, request):
        response = {}
        data = request.data

        try:
            id_restavracija = data['id_restavracija']
            qr = data['qr']
        except KeyError as e:
            response['status'] = 0
            response['description'] = "Missing key data " + str(e) + ""
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if not len(qr):
            response['status'] = 0
            response['description'] = "Missing data"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        table = {
            'id_restavracija': id_restavracija,
            'id_miza': qr
        }

        serializer = MizeSerializer(data=table)
        if serializer.is_valid():
            serializer.save()
            response['status'] = 1
            response['description'] = "Successfully added table to restaurant"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['status'] = 0
            response['description'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


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
            email_error = ("Email - " + serializer.errors['email'][0]) if 'email' in serializer.errors else ""
            password_error = (
                    "Password - " + serializer.errors['password'][0]) if 'password' in serializer.errors else ""

            response['status'] = 0
            response['description'] = "Error: " + email_error + password_error
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UporabnikViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UporabnikSerializer
    queryset = Uporabnik.objects.all()
    model = Uporabnik

    @action(detail=False, methods=['POST'])
    def get_orders(self, request):
        """
        Return all orders and meal data for given user
        """
        response = {}
        try:
            id_uporabnik = request.data['id_uporabnik']
        except KeyError:
            id_uporabnik = None

        try:
            limit = int(request.data['num_orders'])
        except KeyError:
            limit = 10

        if id_uporabnik is None:
            response['status'] = 0
            response['description'] = "Error: Please input the user id"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response['status'] = 1
            response['description'] = "Orders for user: " + id_uporabnik + ""
            response['orders'] = get_orders(id_uporabnik, limit)
            return Response(response, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['POST'])
    def check_in(self, request):
        # TODO: Implement check in from user
        response = {}
        try:
            id_narocila = request.data['id_narocilo']
            qr = request.data['qr']
        except KeyError:
            response['status'] = 0
            response['description'] = "Error: Missing either id_narocilo or qr"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # noinspection PyBroadException
        try:
            order = Narocilo.objects.get(id_narocila=id_narocila)
            order_id_restaurant = order.id_restavracija
        except Exception:
            response['status'] = 0
            response['description'] = "Could not retrieve order {}".format(id_narocila)
            return Response(response, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            Mize.objects.get(id_restavracija=order_id_restaurant, id_miza=qr)
        except models.ObjectDoesNotExist:
            response['status'] = 0
            response['description'] = "Error: Restaurant ID and QR do not match for provided Order"
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        data = model_to_dict(order)
        data["checked_in"] = True
        data["id_miza"] = qr

        serializer = NarociloSerializer(data=data, instance=order)
        if serializer.is_valid():
            serializer.save()
            # Add order to checked_in array to be used in refresh api call
            order_dict = {'id_narocila': order.id_narocila, 'qr': qr,
                          'id_restavracija': order.id_restavracija.id_restavracija}
            add_checked_in_order(order_dict)

            response['status'] = 1
            response['description'] = "Successfully checked in order"
            return Response(response, status=status.HTTP_200_OK)
        else:
            response['status'] = 0
            response['description'] = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class JedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = JedSerializer
    queryset = Jed.objects.all()
    model = Jed

    def list(self, request, *args, **kwargs):
        return_data = defaultdict(list)
        get_params = request.query_params

        try:
            id_restavracija = get_params['id_restavracija']
        except KeyError:
            response = {
                'status': 0,
                'description': "Missing id, add ?id_restavracija=x to call"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        meal_types = JedilniList.objects.all()
        meal_types = JedilniListSerializer(meal_types, many=True).data
        meal_types = {x['id_jedilni_list']: x['vrsta'] for x in meal_types}  # Transform OrderDict to dict

        meals = Jed.objects.filter(id_restavracija=id_restavracija)
        meals = JedSerializer(meals, many=True).data

        for meal in meals:
            typ = meal_types[meal['id_jedilni_list']]
            return_data[typ].append({
                'id_jed': meal['id_jed'],
                'ime_jedi': meal['ime_jedi'],
                'opis_jedi': meal['opis_jedi'],
                'cena': meal['cena'],
                'kolicina': 1
            })

        return Response(return_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def new_meal(self, request):
        """
        Create new meal
        """
        serializer = JedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {'status': 1, 'description': "New meal created"}
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {'status': 0, 'description': "Could not create meal"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
