import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),   # 16
            Player("Lemieux", "PIT", 45, 54), # 99
            Player("Kurri",   "EDM", 37, 53), # 90
            Player("Yzerman", "DET", 42, 56), # 98
            Player("Gretzky", "EDM", 35, 89)  # 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.stats = StatisticsService(PlayerReaderStub())

    #get players (method search)
    def test_search_existing_player(self): 
        player = self.stats.search("Kurri")
        self.assertIsNotNone(player)
        self.assertEqual(player.name, "Kurri")
        self.assertEqual(player.team, "EDM")
        self.assertEqual(player.goals, 37)
        self.assertEqual(player.assists, 53)

    # Testaa search-metodi olemattomalle pelaajalle
    def test_search_nonexistent_player_returns_none(self):
        player = self.stats.search("Noname")
        self.assertIsNone(player)

    # Testaa team-metodi, palauttaa pelaajat tietystä joukkueesta
    def test_team_returns_correct_players(self):
        edm_players = self.stats.team("EDM")
        self.assertEqual(len(edm_players), 3)
        self.assertTrue(all(p.team == "EDM" for p in edm_players))

    # Testaa team-metodi, kun ei ole pelaajia
    def test_team_no_players_returns_empty_list(self):
        players = self.stats.team("NYR")
        self.assertEqual(players, [])

    # Testaa top-metodi, palauttaa oikean määrän pelaajia pistejärjestyksessä
    def test_top_returns_correct_number_of_players(self):
        top3 = self.stats.top(3)
        self.assertEqual(len(top3), 3)
        points = [p.points for p in top3]
        self.assertEqual(points, sorted(points, reverse=True))

    # Testaa top-metodi negatiivisella tai nollalla
    def test_top_handles_zero_or_negative(self):
        top0 = self.stats.top(0)
        self.assertEqual(len(top0), 0)
        top_neg = self.stats.top(-1)
        self.assertEqual(len(top_neg), 0)

    def test_top_by_points(self):
        top = self.stats.top(2, SortBy.POINTS)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[1].name, "Lemieux")

    def test_top_by_goals(self):
        top = self.stats.top(2, SortBy.GOALS)
        self.assertEqual(top[0].name, "Lemieux")
        self.assertEqual(top[1].name, "Yzerman")

    def test_top_by_assists(self):
        top = self.stats.top(2, SortBy.ASSISTS)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[1].name, "Yzerman")

    def test_top_defaults_to_points_when_sortby_not_given(self):
        top = self.stats.top(2)
        self.assertEqual(top[0].name, "Gretzky")
        self.assertEqual(top[1].name, "Lemieux")
    
    