SELECT 
    h.INCOME_RANGE, h.HH_SIZE, h.CHILDREN, t.SPEND, t.UNITS
FROM 
    transactions t 
INNER JOIN 
    households h on 
        t.HSHD_NUM = h.HSHD_NUM;