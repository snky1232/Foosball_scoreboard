import json
import falcon
import pymongo
import os


class GeneralResource:
    def __init__(self, db):
        self.db = db
        self.static_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')


class GameResource(GeneralResource):

    def on_get(self, req, resp):
        index_file = os.path.join(self.static_path, 'index.html')
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open(index_file, 'r') as index:
            resp.body = index.read()

    def on_post(self, req, resp):
        data = req.stream.read(req.content_length or 0)
        try:
            json_data = json.loads(data.decode('utf-8'))
            team1_name = json_data['p1_name'] + ' & ' + json_data['p2_name']
            team1_score = int(json_data['t1_score'])
            team2_name = json_data['p3_name'] + ' & ' + json_data['p4_name']
            team2_score = int(json_data['t2_score'])
        except ValueError:
            raise falcon.HTTPBadRequest()
        try:
            self.db.add_scores(team1_name, team1_score, team2_name, team2_score)
        except pymongo.errors.PyMongoError as e:
            raise falcon.HTTPInternalServerError()
        else:
            resp.body = '{"message": "Done."}'


class ScorePageResource(GeneralResource):

    def on_get(self, req, resp):
        index_file = os.path.join(self.static_path, 'scores.html')
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open(index_file, 'r') as index:
            resp.body = index.read()


class ScoreResource(GeneralResource):

    def on_get(self, req, res):
        data = self.db.get_scores()
        res.body = json.dumps(data)
