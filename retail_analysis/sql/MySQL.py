from sqlalchemy import create_engine
import pandas as pd
df = pd.read_csv("/Users/lina/Downloads/demand_forecasting.csv")
df['Date'] = pd.to_datetime(df['Date'])

engine = create_engine("mysql+mysqlconnector://root:yzy060624@localhost:3306/demand_db")
try:
    connection = engine.connect()
    print("yes")
    connection.close()
except Exception as e:
    print("no",e)
df.to_sql(name="demand_data", con=engine, if_exists="replace", index=False)
print(df.columns.str.lower())

