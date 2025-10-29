import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):

    def test_player_init_y_get(self):
        p = Player("Luchito")
        self.assertEqual(p.get_name(), "Luchito")

    def test_player_set_name(self):
        p = Player("Luchito")
        p.set_name("Lucas")
        self.assertEqual(p.get_name(), "Lucas")

    def test_player_repr(self):
        p = Player("Luchito")
        self.assertEqual(repr(p), "Player: Luchito")
        p.set_name("Lucas")
        self.assertEqual(repr(p), "Player: Lucas")  
    
