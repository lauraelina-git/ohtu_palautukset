import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from player import Player

console = Console()


class PlayerReader:  # pylint: disable=too-few-public-methods
    def __init__(self, url: str):
        self.url = url

    def get_players(self):
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return [Player(p) for p in data]


class PlayerStats:
    def __init__(self, reader):
        self.players = reader.get_players()

    def get_nationalities(self):
        return sorted(set(p.nationality for p in self.players if p.nationality))

    def top_scorers_by_nationality(self, nationality: str):
        filtered = [p for p in self.players if p.nationality == nationality]
        return sorted(filtered, key=lambda p: p.total_points(), reverse=True)


def display_players(players, nationality, season):
    table = Table(
        title=f"Season {season} Players from {nationality}",
        header_style="bold magenta",
        box=box.SIMPLE_HEAVY,
    )
    table.add_column("Name", style="cyan")
    table.add_column("Team", style="green")
    table.add_column("Goals", justify="right")
    table.add_column("Assists", justify="right")
    table.add_column("Points", justify="right")

    for p in players:
        table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(p.total_points()))

    console.print(table)


def choose_season():
    seasons = [
        "2018-19", "2019-20", "2020-21", "2021-22",
        "2022-23", "2023-24", "2024-25",
    ]
    return Prompt.ask("\nChoose a season", choices=seasons, default="2024-25")


def choose_nationality(nationalities):
    return Prompt.ask("\nChoose nationality", choices=nationalities, default="FIN").upper()


def fetch_stats(season):
    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    console.print(f"[dim]Fetching data from {url}[/dim]")
    return PlayerStats(PlayerReader(url))


def show_results(stats, season):
    nationality = choose_nationality(stats.get_nationalities())
    players = stats.top_scorers_by_nationality(nationality)

    if players:
        display_players(players, nationality, season)
    else:
        console.print(f"[yellow]No players found for '{nationality}' in {season}.[/yellow]")


def main():
    console.print("[bold blue]NHL Player Stats Viewer[/bold blue] 🏒")
    season = choose_season()

    try:
        stats = fetch_stats(season)
        show_results(stats, season)
    except requests.RequestException as error:
        console.print(f"[red]Error fetching player data:[/red] {error}")


if __name__ == "__main__":
    main()
