from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import tornado.web
from random import seed
from random import randint

import json

games = []

class Game(RequestHandler):
  def get(self):
    self.write({'games': games})

class Games(RequestHandler):
  def board_value(self):
    b = [' ' for x in range(9)]
    return b

  #creates a new data structure for the game
  def new_game(self):
    id =randint(0, 1000000) #id assumes not repeated number
    board= self.board_value() 
    k_v={}  #game dictionary indexed by id
    k_match={} #match data
    k_v['gid']=id
    k_v['match']=k_match
    k_match['playerX']= "name1"
    k_match['playerO']= "name2"
    k_match['winner']=  "pending"
    k_match['board']=board
    json_string=json.dumps(k_v)
    return json_string  #returns game in json format

  # get value for a new game or display a game based on id  
  def get(self,id):
    if (id is None):  #creates a new game
        g = self.new_game()
        games.append(g)
        self.write({'debug': 'new game added'})
    else:
        for i,x in enumerate(games):   #search specific  game
           data = json.loads(x)
           if data['gid'] == int(id):
              self.write(x)
              return	
        raise tornado.web.HTTPError(404)	 # game not found
  #updates a game
  def post(self,id):
    found = None
    #updates a value for a game    
    for i,x in enumerate(games):
       data = json.loads(x)
       if int(data['gid']) == int(id):
          found = data
          to_change = found
          data['match'] = json.loads(self.request.body)
          y=json.dumps(data) #saves  uploaded value
          games[i]=y #insert values in array
          return
    self.write({'debug': 'new game added'})

# Simple Tornado base handler with error handling
class BaseHandler(tornado.web.RequestHandler):
    def __init__(self,application, request,**kwargs):
        super(BaseHandler,self).__init__(application,request)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('errors/404.html',page=None)
        else:
            self.render('errors/unknown.html',page=None)
def make_app():
  urls = [
    ("/", Game),    
    (r"/api/games/([^/]+)?", Games)
  ]
  return Application(urls, debug=True)
  
if __name__ == '__main__':
  app = make_app()
  app.listen(8888)
  IOLoop.instance().start()
