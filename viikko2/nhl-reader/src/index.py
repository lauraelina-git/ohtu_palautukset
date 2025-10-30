import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players = [Player(p) for p in response]

    # Suodatetaan suomalaiset
    finnish_players = [p for p in players if p.nationality == "FIN"]

    print("Players from FIN:")
    for player in finnish_players:
        print(player)


if __name__ == "__main__":
    main()
