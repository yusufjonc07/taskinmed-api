from sqlalchemy import inspect
from urllib import request
import time
from sqlalchemy import create_engine
import threading

DBPASS = ".."
DBUSERNAME = ".."
HOST = ".."
DB1 = "..."
PORT = ".."

DBUSERNAME_b = ".."
DBPASS_b = ".."
DB2 = "..."
PORT_b = ".."
HOST_b = ".."


def blocking_io():
    return 'blocking'
    
def net_connect():
    try:
        request.urlopen('http://google.com')
        return True
    except:
        return False



def run_db_code():
    #configure local server
    if len(DBPASS) == 0:

        usrpas = DBUSERNAME
    else:
        usrpas = f"{DBUSERNAME}:{DBPASS}"

    engine = create_engine(f"mysql+pymysql://{usrpas}@{HOST}:{PORT}/{DB1}")

    with engine.connect() as con:


        #configure gloabal server
        if len(DBPASS_b) == 0:
            usrpas_b = DBUSERNAME_b
        else:
            usrpas_b = f"{DBUSERNAME_b}:{DBPASS_b}"

        rmt_engine = create_engine(f"mysql+pymysql://{usrpas_b}@{HOST_b}:{PORT_b}/{DB2}")
        

        if net_connect():
            with rmt_engine.connect() as con2:

                inspector = inspect(rmt_engine)
                TABLES = inspector.get_table_names(schema=DB1)

                while True:

                    time.sleep(3.0)



                    if net_connect() == False:
                        print("no connection")
                    else:

                        try:
                                                    
                            avilable = 0

                            for table_name in TABLES:
                                
                                statement = f"SELECT id FROM {table_name} WHERE uploaded = 0"
                                
                                items = con.execute(statement).all()

                                avilable = avilable + len(items)

                            
                            if avilable > 0:

                                soon = 0
                                
                                for table_name in TABLES:

                                    statement = f"SELECT * FROM {table_name} WHERE uploaded = 0"
                                    
                                    items = con.execute(statement)
                                    

                                    for item in items:

                                       

                                        cols = inspector.get_columns(table_name, schema=DB1)
                                        
                                        stmt1 = f"UPDATE {table_name} SET"
                                        stmt2 = f"INSERT INTO {table_name} ("
                                        stmt2_b = 'VALUES ('

                                        cols_len = len(cols)

                                        for i in range(cols_len):

                                            column = cols[i]

                                            col_name = str(column['name'])
                                            
                                            if col_name != 'id': 
                                                
                                                stmt1 = stmt1 + f" {col_name} = '{item[col_name]}'"

                                                if i != (cols_len-1): 
                                                    stmt1 = stmt1 + ','
                                                else:
                                                    stmt1 = stmt1 + f" WHERE id = {item['id']}"

                                            stmt2 = stmt2 + col_name
                                            stmt2_b = stmt2_b + f"'{item[col_name]}'"

                                            if i != (cols_len-1): 
                                                stmt2 = stmt2 + ', '
                                                stmt2_b = stmt2_b + ', '
                                            else:
                                                stmt2 = stmt2 + ') '
                                                stmt2_b = stmt2_b + ')'

                                        stmt2 = stmt2 + stmt2_b
                                        
                                        statement2 = f"SELECT id FROM {table_name} WHERE id = {item['id']}"
                                        item_yes = con2.execute(statement2).first()
                                        
                                        if item_yes:
                                            result = con2.execute(stmt1)
                                        else:
                                            result = con2.execute(stmt2)

                                        if result:
                                            con.execute(f"UPDATE {table_name} SET uploaded = 1 WHERE id = {item['id']}")
                                            soon = soon + 1

                        
                        except Exception as e:
                            print(e)

run_db_code()        





    

        







        




    

        







