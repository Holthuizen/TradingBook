import streamlit as st
from datetime import date
import sqlite3 

DATABASE_NAME = "options1.db"

tab1, tab2, tab3, tab4 = st.tabs(["Add Option", "Portfolio", "Performance", "Close"])


import streamlit.components.v1 as components

#renders out the order history and portfolio
def render_order_card(row):
    return f"""
    <div style="
        border:1px solid #ddd;
        padding:16px;
        border-radius:12px;
        margin-bottom:12px;
        font-family: sans-serif;
        background-color:#f9f9f9;">
        <h4 style="margin:0;">{row[1]} ({row[2].upper()} - {row[3].upper()})</h4>
        <p style="margin:4px 0;"><strong>Strike:</strong> {row[4]} | <strong>Expiry:</strong> {row[5]}</p>
        <p style="margin:4px 0;"><strong>Qty:</strong> {row[6]} | <strong>Price:</strong> ${row[7]} | <strong>Cost:</strong> ${row[8]}</p>
        <p style="font-size: 0.8em; color: #666;">{row[9]}</p>
        <button>CLOSE POSITION</button>
    </div>
    """


con = sqlite3.connect(DATABASE_NAME) 
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS option_orders (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    option_type TEXT CHECK(option_type IN ('call', 'put')) NOT NULL,
    action TEXT CHECK(action IN ('buy', 'sell')) NOT NULL,
    strike_price REAL NOT NULL,
    expiry_date TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    costs REAL NOT NULL,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
""")

con.commit()


#add bought option contract to db
with tab1: 
    with st.form("option_order_form"):
        symbol = st.text_input("Symbol", value="AMD")
        option_type = st.selectbox("Option Type", ["call", "put"])
        action = st.selectbox("Action", ["buy", "sell"])
        strike_price = st.number_input("Strike Price", min_value=0.0, step=0.5)
        expiry_date = st.date_input("Expiry Date", value=date(2025, 5, 25))
        quantity = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Price per Contract", min_value=0.0, step=0.1)
        costs = st.number_input("Total Costs", min_value=0.0, step=0.1)
        
        submitted = st.form_submit_button("Submit Order")
        
        if submitted:
            #feedback
            st.write("Order submitted:")
            st.write({
                "symbol": symbol,
                "option_type": option_type,
                "action": action,
                "strike_price": strike_price,
                "expiry_date": expiry_date.isoformat(),
                "quantity": quantity,
                "price": price,
                "costs": costs, 
                "close_prise": 0, #unknown
            }) 
            #update database
            con = sqlite3.connect(DATABASE_NAME) 
            cur = con.cursor()
            cur = con.cursor()
            cur.execute(
                """INSERT INTO option_orders (
                    symbol, option_type, action,
                    strike_price, expiry_date,
                    quantity, price, costs
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    symbol, option_type, action,
                    strike_price, expiry_date.isoformat(),
                    quantity, price, costs
                )
            )
            con.commit()


#see all open option contracts in portfolio
with tab2: 
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    cur.execute("SELECT * FROM option_orders")
    rows = cur.fetchall()

    for row in rows:
        components.html(render_order_card(row), height=200)





#compute the buy vs sell price 
with tab3: 
    pass


with tab4: 
    pass 