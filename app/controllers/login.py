from blacksheep.server.controllers import Controller, get, post
from blacksheep import Request, redirect
from app.env import DB_CONN_STR
import psycopg2 as pg
import bcrypt


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

        with pg.connect(DB_CONN_STR) as conn:
            cur = conn.cursor()
            cur.execute("SELECT password, email FROM users WHERE username=%s", (username,))
            u = cur.fetchone()

        if u is not None and bcrypt.checkpw(password, u[0].tobytes()) and email == u[1]:
            # success
            session = req.session
            session.set("auth", True)
            return redirect(f"/home/{username}")
        else:
            # failure
            return self.view("index", {"error": "INVALID CREDENTIALS"}, request=req)
