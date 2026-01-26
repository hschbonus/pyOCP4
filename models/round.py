from .match import Match
from datetime import datetime


class Round:
    def __init__(self,
                 name,
                 match_list=None):
        self.name = name
        self.start_date_time = datetime.now().replace(microsecond=0)
        self.end_date_time = None
        self.match_list = match_list if match_list is not None else []

    def __repr__(self):
        return f"{self.name}"

    def to_dict(self):
        serializable_match_list = []
        for match in self.match_list:
            serializable_match_list.append(match.to_dict())

        round_dict = {
            'name': self.name,
            'start_date_time': str(self.start_date_time),
            'end_date_time': str(self.end_date_time),
            'match_list': serializable_match_list
        }
        return round_dict

    @classmethod
    def from_dict(cls, round_dict):
        round = cls(
            name=round_dict["name"],
            match_list=[Match.from_dict(m) for m in round_dict["match_list"]]
        )

        round.start_date_time = datetime.fromisoformat(round_dict["start_date_time"])
        round.end_date_time = 'None'
        return round

    def create_match(self, player1, player2):
        match = Match(player1, player2)
        self.match_list.append(match)
        return match

    def mark_as_complete(self):
        self.end_date_time = datetime.now().replace(microsecond=0)
