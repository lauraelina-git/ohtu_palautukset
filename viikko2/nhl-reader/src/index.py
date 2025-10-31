import requests
from player import Player

class PlayerReader:
    def __init__(self, url: str):
        self.url = url
    
    def get_players(self):
        response = requests.get(self.url)
        response.raise_for_status()
        data = response.json()
        return [Player(p) for p in data]

class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality: str):
        filtered = [p for p in self.players if p.nationality == nationality]
        return sorted(filtered, key=lambda p: p.total_points(), reverse=True)

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality("FIN")

    for player in players:
        print(player)

if __name__ == "__main__":
    main()
