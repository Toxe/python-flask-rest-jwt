from app.models import Ship, list_ships, find_ship, get_next_ship_id, add_new_ship, replace_existing_ship


def test_list_ships_returns_list():
    ships = list_ships()
    assert len(ships) > 0
    assert type(ships[0]) is Ship


def test_find_existing_ship():
    ship = find_ship(1)
    assert ship != None
    assert type(ship) is Ship
    assert ship.id == 1


def test_find_non_existing_ship():
    ship = find_ship(1000)
    assert ship == None


def test_get_next_ship_id_from_populated_list():
    ships = [
        Ship(id=3, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[]),
        Ship(id=7, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[]),
    ]
    assert get_next_ship_id(ships) == 8


def test_get_next_ship_id_from_empty_list():
    ships = []
    assert get_next_ship_id(ships) == 1


def test_add_new_ship():
    ship = Ship(id=0, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[])
    ship = add_new_ship(ship)
    assert ship.id > 0


def test_add_new_ship_with_nonzero_id():
    ship = Ship(id=20, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[])
    assert add_new_ship(ship) == None


def test_add_new_ship_with_none_argument():
    assert add_new_ship(None) == None


def test_replace_existing_ship():
    ship1 = Ship(id=5, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    assert replace_existing_ship(ship1)
    ship2 = find_ship(5)
    assert ship1.id == ship2.id
    assert ship1.model == ship2.model


def test_replace_existing_ship_with_bad_id():
    ship1 = Ship(id=0, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    ship2 = Ship(id=-1, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    assert replace_existing_ship(ship1) == False
    assert replace_existing_ship(ship2) == False


def test_replace_existing_ship_with_none_argument():
    assert replace_existing_ship(None) == False
