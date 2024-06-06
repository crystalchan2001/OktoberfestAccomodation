from mapper import Mapper
import pytest

map1 = Mapper(('48.1647', '11.5724'), "Schwabing-West") #
map2 = Mapper(('48.10996', '11.59264'), None)
map3 = Mapper(None, "Schwabing-West")
map4 = Mapper(None, None)

class TestMapper:

    @pytest.mark.parametrize("inputA, expectedA, name", [
        (map1, 4.06, "map1"),
        (map2, 3.99, "map2"),
        (map3, None, "map3"),
        (map4, None, "map4")
    ])

    def test_distance(self, inputA, expectedA, name):
        distance = inputA.getDistance()
        assert distance == expectedA

    @pytest.mark.parametrize("inputB, expectedB, name", [
        (map1, 4.34, "map1"),
        (map2, None, "map2"),
        (map3, 4.34, "map3"),
        (map4, None, "map4")
    ])

    def test_distance_name(self, inputB, expectedB, name):
        distance = inputB.getDistanceFromName()
        assert distance == expectedB

    @pytest.mark.parametrize("inputC, expectedC, name", [
        (map1, list, "map1"),
        (map2, list,  "map2"),
        (map3, type(None), "map3"),
        (map4, type(None), "map4")
    ])

    def test_commute(self, inputC, expectedC, name):
        calculated = inputC.getCommute()
        assert type(calculated[0]) == expectedC and type(calculated[1]) == expectedC
