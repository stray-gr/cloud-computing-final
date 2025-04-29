from blacksheep.server.controllers import Controller, get
from blacksheep import Request, redirect

class Home(Controller):
    @get("/home/{username}")
    def index(self, req: Request):
        session = req.session
        if not session.get("auth", False): 
            # not auth
            return redirect("/")
        return self.view("index", {"name": req.route_values["username"]}, request=req)