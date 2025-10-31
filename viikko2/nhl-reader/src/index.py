import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from player import Player

console = Console()


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

    def get_nationalities(self):
        """Palauttaa listan kaikista kansallisuuksista."""
        return sorted(set(p.nationality for p in self.players if p.nationality))

    def top_scorers_by_nationality(self, nationality: str):
        """Palauttaa suodatetut ja järjestetyt pelaajat."""
        filtered = [p for p in self.players if p.nationality == nationality]
        return sorted(filtered, key=lambda p: p.total_points(), reverse=True)


def display_players(players, nationality, season):
    """Tulostaa pelaajat Rich-taulukkona."""
    table = Table(
        title=f"Season {season} Players from {nationality} ",
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
    )
    table.add_column("Name", style="cyan")
    table.add_column("Team", style="green")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for p in players:
        table.add_row(
            p.name,
            p.team,
            str(p.goals),
            str(p.assists),
            str(p.total_points())
        )

    console.print(table)


def main():
    console.print("[bold blue]NHL Player Stats Viewer[/bold blue] 🏒")

    # Näytetään käyttäjälle tarjolla olevat kaudet (API-tiedossa)
    available_seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
    season = Prompt.ask("\nChoose a season", choices=available_seasons, default="2024-25")

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    console.print(f"[dim]Fetching data from {url}[/dim]")

    try:
        reader = PlayerReader(url)
        stats = PlayerStats(reader)
        nationalities = stats.get_nationalities()

        nationality = Prompt.ask("\nChoose nationality", choices=nationalities, default="FIN").upper()

        players = stats.top_scorers_by_nationality(nationality)

        if not players:
            console.print(f"[yellow]No players found for nationality '{nationality}' in season {season}.[/yellow]")
        else:
            display_players(players, nationality, season)

    except requests.RequestException as e:
        console.print(f"[red]Error fetching player data:[/red] {e}")


if __name__ == "__main__":
    main()