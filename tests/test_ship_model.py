from app import db
from app.models import Ship


def test_all_users_returns_list():
    ships = db.all_ships()
    assert len(ships) > 0
    assert type(ships[0]) is Ship


def test_find_existing_ship():
    ship = db.get_ship(1)
    assert ship != None
    assert type(ship) is Ship
    assert ship.id == 1


def test_find_non_existing_ship():
    ship = db.get_ship(1000)
    assert ship == None


def test_get_next_ship_id_from_populated_list():
    ships = [
        Ship(id=3, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[]),
        Ship(id=7, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[]),
    ]
    assert db.get_next_ship_id(ships) == 8


def test_get_next_ship_id_from_empty_list():
    ships = []
    assert db.get_next_ship_id(ships) == 1


def test_add_ship():
    ship = Ship(id=0, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[])
    ship = db.add_ship(ship)
    assert ship.id > 0


def test_add_ship_with_nonzero_id():
    ship = Ship(id=20, affiliation="", category="", crew=0, length=0, manufacturer="", model="", ship_class="", roles=[])
    assert db.add_ship(ship) == None


def test_add_ship_with_none_argument():
    assert db.add_ship(None) == None


def test_update_ship():
    ship1 = Ship(id=5, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    assert db.update_ship(ship1)
    ship2 = db.get_ship(5)
    assert ship1.id == ship2.id
    assert ship1.model == ship2.model


def test_update_non_existing_ship():
    ship = Ship(id=99, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    assert db.update_ship(ship) == False


def test_update_ship_with_bad_id():
    ship1 = Ship(id=0, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    ship2 = Ship(id=-1, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    assert db.update_ship(ship1) == False
    assert db.update_ship(ship2) == False


def test_update_ship_with_none_argument():
    assert db.update_ship(None) == False


def test_delete_ship():
    old_len = len(db.all_ships())
    ship = Ship(id=0, affiliation="?", category="?", crew=1, length=1, manufacturer="?", model="?", ship_class="?", roles=["?"])
    ship = db.add_ship(ship)
    assert ship.id > 0
    assert db.delete_ship(ship.id)
    assert db.get_ship(ship.id) == None
    assert len(db.all_ships()) == old_len


def test_delete_ship_with_bad_id():
    assert db.delete_ship(0) == False
    assert db.delete_ship(-1) == False
    assert db.delete_ship(99) == False
