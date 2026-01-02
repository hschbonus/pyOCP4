class Round:
    def __init__(self,
                 name,
                 start_date_time=None,
                 end_date_time=None,
                 match_list=None):
        if match_list is None:
            match_list = []
        self.name = name
        self.start_date_time = start_date_time  # Auto-rempli quand le round commence
        self.end_date_time = end_date_time  # Auto-rempli quand terminé
        self.match_list = match_list

    def add_match(self, match):
        self.match_list.append(match)

    def mark_as_complete(self):
        from datetime import datetime
        self.end_date_time = datetime.now()