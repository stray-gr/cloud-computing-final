from blacksheep.server.controllers import Controller, get
from blacksheep import Request, redirect
from app.env import DB_NAME, DB_USER, DB_PASS, DB_HOST
import pandas as pd
import psycopg2 as pg

class Metrics(Controller):
    @get("/metrics")
    def index(self, req: Request):
        # Check auth
        session = req.session
        if not session.get("auth", False): 
            return redirect("/")

        # Query
        with pg.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) as conn:
            query = \
            ''' 
            SELECT 
                h.INCOME_RANGE, h.HH_SIZE, h.CHILDREN, t.SPEND, t.STORE_R
            FROM 
                transactions t 
            INNER JOIN households h on t.HSHD_NUM = h.HSHD_NUM;
            '''
            df = pd.read_sql(query, conn)

        # Plot
        income_spend = df[["income_range", "spend"]].groupby("income_range").sum()
        size_spend = df[["hh_size", "spend"]].groupby("hh_size").sum()
        children_spend = df[["children", "spend"]].groupby("children").sum()
        store_spend = df[["store_r", "spend"]].groupby("store_r").sum()

        return self.view(
            name="index", 
            request=req, 
            model={
                "income": income_spend.to_html(header=False, index_names=False, justify="center"),
                "size": size_spend.to_html(header=False, index_names=False, justify="center"),
                "children": children_spend.to_html(header=False, index_names=False, justify="center"),
                "store": store_spend.to_html(header=False, index_names=False, justify="center")
            }
        )
