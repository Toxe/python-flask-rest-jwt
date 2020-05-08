from app.models import list_ships, find_ship


def test_list_ships_returns_list():
    ships = list_ships()
    assert len(ships) > 0


def test_find_existing_ship():
    ship = find_ship(1)
    assert ship != None
    assert ship["id"] == 1


def test_find_non_existing_ship():
    ship = find_ship(1000)
    assert ship == None
