class TennisGame:

    SCORE_NAMES = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = 0
        self.player2_score = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score += 1
        else:
            self.player2_score += 1

    def get_score(self):
        if self.player1_score == self.player2_score:
            return self._score_when_tied()
        elif self.player1_score >= 4 or self.player2_score >= 4:
            return self._score_at_game_end()
        else:
            return self._score_during_game()

    def _score_when_tied(self):
        if self.player1_score < 3:
            return f"{self.SCORE_NAMES[self.player1_score]}-All"
        return "Deuce"

    def _score_at_game_end(self):
        score_diff = self.player1_score - self.player2_score
        if score_diff == 1:
            return "Advantage player1"
        elif score_diff == -1:
            return "Advantage player2"
        elif score_diff >= 2:
            return "Win for player1"
        else:
            return "Win for player2"

    def _score_during_game(self):
        return f"{self.SCORE_NAMES[self.player1_score]}-{self.SCORE_NAMES[self.player2_score]}"
