import configparser
import falcon

from storage import StorageEngine
from resources import GameResource, ScoreResource, ScorePageResource


# read configuration
config = configparser.ConfigParser()
config.read("config.ini")

# get mongo conf
storage_section = config['Mongo']
storage_conf = storage_section['MONGO_CONNECT_URI']
db = StorageEngine(storage_conf)


# init routes
game_resource = GameResource(db)
score_page_resource = ScorePageResource(db)
score_resource = ScoreResource(db)

# init app
app = falcon.API()

# add routes
app.add_route('/', game_resource)
app.add_route('/score', score_page_resource)
app.add_route('/score/data', score_resource)
