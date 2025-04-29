from blacksheep.server.controllers import Controller, get, post
from blacksheep import Request, redirect
import bcrypt, sqlite3


class Login(Controller):
    @get("/")
    def index(self, req: Request):
        return self.view("index", {"error": ""}, request=req)

    @post("/auth-user")
    async def auth_user(self, req: Request):
        form = await req.form()
        username = form["username"]
        password = form["password"].encode("utf-8")
        email = form["email"]

        with sqlite3.connect("proj.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT password, email FROM users WHERE username=?", (username,))
            user = cur.fetchone()

        if user is not None and bcrypt.checkpw(password, user[0]) and email == user[1]:
            # success
            session = req.session
            session.set("auth", True)
            return redirect(f"/home/{username}")
        else:
            # failure
            return self.view("index", {"error": "INVALID CREDENTIALS"}, request=req)
