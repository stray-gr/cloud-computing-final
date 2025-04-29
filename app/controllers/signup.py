from blacksheep.server.controllers import Controller, get, post
from blacksheep import Request, redirect
import bcrypt, sqlite3


class Signup(Controller):
    @get("/signup")
    def index(self, req: Request):
        return self.view("index", {}, request=req)

    @post("/new-user")
    async def new_user(self, req: Request):
        form = await req.form()
        username = form["username"]
        password = form["password"]
        confirm  = form["confirm"]
        email    = form["email"]

        with sqlite3.connect("proj.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT password, email FROM users WHERE username=?", (username,))
            user = cur.fetchone()

        if user is None and password == confirm:
            # success
            pass_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            pass_hash = bcrypt.hashpw(pass_bytes, salt)

            with sqlite3.connect("proj.db") as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users(username, password, email) VALUES(?, ?, ?)", 
                    (username, pass_hash, email)
                )
                conn.commit()

            session = req.session
            session.set("auth", True)
            return redirect(f"/home/{username}")

        elif user is not None:
            # username taken
            return self.view("index", {"error": "USERNAME TAKEN"}, request=req)

        else:
            # password mismatch
            return self.view("index", {"error": "PASSWORDS DON'T MATCH"}, request=req)
