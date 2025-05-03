from blacksheep.server.controllers import Controller, get
from blacksheep import Request, Response, redirect
from app.env import DB_NAME, DB_USER, DB_PASS, DB_HOST
import psycopg2 as pg


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
    @get("/dash")
    def index(self, req: Request):
        session = req.session
        if not session.get("auth", False): 
            # not auth
            return redirect("/")

        hshd_num = req.query.get("hshd", ["0010"])[0]
        offset = 0

        with pg.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
            cur = conn.cursor()

            cur.execute("SELECT DISTINCT HSHD_NUM FROM households ORDER BY HSHD_NUM ASC;")
            hshd_list = list(map(lambda r: r[0], cur.fetchall()))[:-1]

            cur.execute(
                '''
                    SELECT 
                        h.*, p.*, t.BASKET_NUMBER, t.SPEND, t.UNITS, t.STORE_R, t.PURCHASE, t.YEAR
                    FROM 
                        transactions t 
                    INNER JOIN 
                        households h on 
                            t.HSHD_NUM = h.HSHD_NUM and 
                            t.HSHD_NUM like %s
                    INNER JOIN
                        products p on
                            t.PRODUCT_NUM = p.PRODUCT_NUM
                    LIMIT 10 OFFSET %s;
                ''',
                (hshd_num, offset,)
            )
            rows = cur.fetchall()

        return self.view(
            name="index", 
            request=req,
            model={
                "hshd_list": hshd_list,
                "row_count": len(rows),
                "offset": offset,
                "hshd": hshd_num,
                "header": HEADER, 
                "rows": rows, 
            }, 
        )

    @get("/dash/data/{hshd_num}/{offset}")
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

        with pg.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
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
                            t.HSHD_NUM like %s
                    INNER JOIN
                        products p on
                            t.PRODUCT_NUM = p.PRODUCT_NUM
                    LIMIT 10 OFFSET %s;
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

    @get("/dash/latest/{hshd_num}")
    def latest(self, req: Request):
        session = req.session
        if not session.get("auth", False): 
            # not auth
            return redirect("/")

        hshd_num = req.route_values["hshd_num"]
        count_str = req.query.get("count", ["10"])[0]

        try:
            count = int(count_str)
        except (TypeError, ValueError):
            count = 10

        if count < 0:
            return Response(204)

        with pg.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
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
                            t.HSHD_NUM like %s
                    INNER JOIN
                        products p on
                            t.PRODUCT_NUM = p.PRODUCT_NUM
                    ORDER BY PURCHASE DESC;
                ''',
                (hshd_num,)
            )
            rows = cur.fetchmany(count)

        return self.view(
            name="latest", 
            request=req,
            model={
                "hshd": hshd_num,
                "count": count,
                "header": HEADER, 
                "rows": rows, 
            }, 
        )
