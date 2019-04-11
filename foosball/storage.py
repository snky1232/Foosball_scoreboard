from pymongo import MongoClient, DESCENDING


class StorageEngine:
    def __init__(self, connection_string):
        self.client = MongoClient(connection_string)
        self.db = self.client['foosball']['teams']  # this is a collection

    def add_scores(self, team1_name, team1_score, team2_name, team2_score):
        self.db.update_one({'team_name': team1_name}, {
                '$inc': {
                    'total_score': team1_score
                }},
                 upsert=True)
        self.db.update_one({'team_name': team2_name}, {
            '$inc': {
                'total_score': team2_score
            }},
            upsert=True)

    def get_scores(self):
        return list(self.db.find({}, {
            '_id': 0,
            'team_name': 1,
            'total_score': 1
        }).sort('total_score', DESCENDING))


