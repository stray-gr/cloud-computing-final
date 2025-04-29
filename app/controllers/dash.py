from blacksheep.server.controllers import Controller, get
from blacksheep import Request, Response, redirect
import sqlite3


HEADER = [
    "HH No.",
    "Loyalty",
    "Age Range",
    "Marital Status",
    "Income Range",
    "Homeowner",
    "Occupants",
    "Size",
    "Children",
    "Product No.",
    "Department",
    "Commodity",
    "Brand Type",
    "Organic",
    "Basket No.",
    "Spend",
    "Units",
    "Region",
    "Date",
    "Year",
]


class Dash(Controller):
    @get("/dash/{hshd_num}")
    def index(self, req: Request):
        session = req.session
        if not session.get("auth", False): 
            # not auth
            return redirect("/")

        hshd_num = req.route_values["hshd_num"]
        offset = 0

        # SELECT DISTINCT HSHD_NUM FROM households;
        with sqlite3.connect("proj.db") as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                    SELECT 
                        h.*, p.*, t.BASKET_NUMBER, t.SPEND, t.UNITS, t.STORE_R, t.PURCHASE, t.YEAR
                    FROM 
                        transactions t 
                    INNER JOIN 
                        households h on 
                            t.HSHD_NUM = h.HSHD_NUM and 
                            t.HSHD_NUM like ?
                    INNER JOIN
                        products p on
                            t.PRODUCT_NUM = p.PRODUCT_NUM
                    LIMIT 10 OFFSET ?;
                ''',
                (hshd_num, offset,)
            )
            rows = cur.fetchall()

        return self.view(
            name="index", 
            request=req,
            model={
                "hshd": hshd_num,
                "offset": offset,
                "header": HEADER, 
                "rows": rows, 
                "row_count": len(rows),
            }, 
        )

    @get("/dash/{hshd_num}/{offset}")
    def data(self, req: Request):
        session = req.session
        if not session.get("auth", False): 
            # not auth
            return redirect("/")

        hshd_num = req.route_values["hshd_num"]
        offset_str = req.route_values["offset"]

        try:
            offset = int(offset_str)
        except (TypeError, ValueError):
            offset = 0

        if offset < 0:
            return Response(204)

        with sqlite3.connect("proj.db") as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                    SELECT 
                        h.*, p.*, t.BASKET_NUMBER, t.SPEND, t.UNITS, t.STORE_R, t.PURCHASE, t.YEAR
                    FROM 
                        transactions t 
                    INNER JOIN 
                        households h on 
                            t.HSHD_NUM = h.HSHD_NUM and 
                            t.HSHD_NUM like ?
                    INNER JOIN
                        products p on
                            t.PRODUCT_NUM = p.PRODUCT_NUM
                    LIMIT 10 OFFSET ?;
                ''',
                (hshd_num, offset,)
            )
            rows = cur.fetchall()

        return self.view(
            name="data", 
            request=req,
            model={
                "hshd": hshd_num,
                "offset": offset,
                "header": HEADER, 
                "rows": rows, 
                "row_count": len(rows),
            }, 
        )
