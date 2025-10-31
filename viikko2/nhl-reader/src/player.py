class Player:
    
    def __init__(self, data: dict):
        # Attribuutit, joita ohjelmassa tarvitaan
        self.name = data.get("name")
        self.nationality = data.get("nationality")
        self.team = data.get("team")
        self.goals = data.get("goals", 0)
        self.assists = data.get("assists", 0)

    def total_points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name:20} team {self.team}  {self.goals} + {self.assists} = {self.total_points()}"
    