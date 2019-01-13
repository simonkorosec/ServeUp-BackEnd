import copy
from collections import defaultdict

from ServeUp.serializers import *

# Dictionary that holds an array of every new order created since last check for each restaurant
new_orders = defaultdict(list)

# Dictionary that holds an array of every cancelled order since last check for each restaurant
cancelled_orders = defaultdict(list)

# Dictionary that holds an array of every checked in order since last check for each restaurant
checked_in_orders = defaultdict(list)

# Constants for order status
ORDER_NEW = 0  # "Nova Naročila"
ORDER_PREPARING = 1  # "V Pripravi"
ORDER_DONE = 2  # "Pripravljeno"
ORDER_FINISHED = 3  # "Končano"


def add_new_order(order):
    """
    Add new order to list
    :param order: Dictionary that hold the order details
    """
    new_orders[order['id_restavracija']].append(order)


def add_checked_in_order(order):
    """
    Add new order to list
    :param order: Dictionary that holds the order details
    """
    checked_in_orders[order['id_restavracija']].append({'id_narocila': order['id_narocila'], 'qr': order['qr']})


def add_cancelled_order(order):
    """
    Add a cancelled order to list
    :param order: Dictionary that hold the order details
    """
    cancelled_orders[order['id_restavracija']].append(order['id_narocila'])


def get_new_cancelled_checked_in_orders(restaurant_id):
    """
    Return all three arrays and reset new_orders, cancelled_orders and checked_in_orders for specific restaurant
    :return: Tuple of (new_orders, cancelled_orders, checked_in_orders)
    """
    tmp_new = copy.deepcopy(new_orders[restaurant_id])
    tmp_cancelled = copy.deepcopy(cancelled_orders[restaurant_id])
    tmp_checked_in = copy.deepcopy(checked_in_orders[restaurant_id])
    new_orders[restaurant_id].clear()
    cancelled_orders[restaurant_id].clear()
    checked_in_orders[restaurant_id].clear()
    return tmp_new, tmp_cancelled, tmp_checked_in


def get_restaurants(location):
    """
    Helper method that return a list of restaurants in the specified location
    :param location: name of the city
    :return: list of restaurants
    """
    posta = Posta.objects.get(kraj__icontains=location)
    data = RestavracijaPodatki.objects.filter(postna_stevilka=posta.postna_stevilka)
    return RestavracijaPodatkiSerializer(data, many=True).data


def get_orders(id_uporabnik, limit=10):
    """
    Helper method that return a list of orders for a specific user.
    :param id_uporabnik: user id
    :param limit: how many orders to return, default value is 10
    :return: List of most recent orders for a specific user
    """
    response = []

    # Get 'limit' orders for user, sort by time of order descending so we get latest orders
    orders = NarociloSerializer(Narocilo.objects.filter(id_uporabnik=id_uporabnik).order_by('-cas_narocila')[:limit],
                                many=True).data

    for order in orders:
        cena = 0.0
        restaurant_name = RestavracijaSerializer(
            Restavracija.objects.get(id_restavracija=order['id_restavracija'])).data['ime_restavracije']

        if order['status'] == ORDER_NEW:
            status = 0
        elif order['status'] == ORDER_PREPARING or order['status'] == ORDER_DONE:
            status = 1
        else:
            status = 2

        data = {"id_narocila": order['id_narocila'],
                "cas_prevzema": order['cas_prevzema'],
                "cas_narocila": order['cas_narocila'],
                "ime_restavracije": restaurant_name,
                "cena": 0.0,
                "status": status,
                "checked_in": order['checked_in'],
                "jedi": []}

        meals_in_order = NarociloPodatkiSerializer(JediNarocilaPodatki.objects.filter(id_narocila=order['id_narocila']),
                                                   many=True).data

        for meal in meals_in_order:
            meal_data = {
                "id_jed": meal['id_jed'],
                "ime_jedi": meal['ime_jedi'],
                "cena": meal['cena'],
                "opis_jedi": meal['opis_jedi'],
                "kolicina": meal['kolicina']
            }
            cena += meal_data['cena'] * meal_data['kolicina']
            data['jedi'].append(meal_data)

        data['cena'] = cena
        response.append(data)

    return response


def add_meals_to_order(meals, id_narocila):
    """
    Helper method to insert meals of an order
    :param meals: List of meal data
    :param id_narocila: Order id
    :return: True / False if every insertion succeeded
    """
    tmp = []
    price = 0
    for meal in meals:
        data = {
            'id_jed': meal['id_jed'],
            'id_narocila': id_narocila,
            'kolicina': meal['kolicina'],
        }
        serializer = JediNarocilaSerializer(data=data)
        if serializer.is_valid():
            tmp.append(serializer.save())
            price += float(meal['cena'] * meal['kolicina'])

        else:
            # Delete every inserted meal data
            for t in tmp:
                t.delete()
            return False, 0

    return True, price
