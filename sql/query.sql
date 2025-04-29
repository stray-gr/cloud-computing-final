SELECT 
    h.*, p.*, t.BASKET_NUMBER, t.PURCHASE, t.SPEND, t.UNITS, t.STORE_R, t.YEAR
FROM 
    transactions t 
INNER JOIN 
    households h on 
        t.HSHD_NUM = h.HSHD_NUM and 
        t.HSHD_NUM like "0010"
INNER JOIN
    products p on
        t.PRODUCT_NUM = p.PRODUCT_NUM
LIMIT 10 OFFSET 0;