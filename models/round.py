from .match import Match


class Round:
    def __init__(self,
                 name,
                 start_date_time=None,
                 end_date_time=None,
                 match_list=None):
        if match_list is None:
            match_list = []
        self.name = name
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.match_list = match_list

    def __repr__(self):
        return f"{self.name}"

    def create_match(self, player1, player2):
        match = Match(player1, player2)
        self.match_list.append(match)
        return match

    def mark_as_complete(self):
        from datetime import datetime
        self.end_date_time = datetime.now()
