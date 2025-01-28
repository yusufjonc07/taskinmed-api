from sqlalchemy import inspect
from urllib import request
import time
from sqlalchemy import create_engine
import sched, time

DBPASS = "Klinika#123"
DBUSERNAME = "root"
HOST = "localhost"
DB1 = "klinika"
PORT = 3306

DBUSERNAME_b = "root"
DBPASS_b = "crudgroup"
DB2 = "klinika_taskin"
PORT_b = 3306
HOST_b = "185.196.214.61"

s = sched.scheduler(time.time, time.sleep)


def blocking_io():
    return 'blocking'
    
def net_connect():
    try:
        request.urlopen('http://google.com')
        print("Internet YES")
        return True
    except:
        return False



def run_db_code(sc):
    #configure local server
    
    if len(DBPASS) == 0:

        usrpas = DBUSERNAME
    else:
        usrpas = f"{DBUSERNAME}:{DBPASS}"
    # print(f"mysql+pymysql://{usrpas}@{HOST}:{PORT}/{DB1}")
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
                TABLES = inspector.get_table_names(schema=DB2)


                time.sleep(5.0)

                if net_connect() == False:
                    print("NO Internet")
                else:

                    try:

                        items_del = con.execute(f"SELECT * FROM deleteds")

                        for del_item in items_del:
                            try:
                                del_stmt = f"DELETE FROM `{del_item['table']}` WHERE `{del_item['table']}`.`id` = {del_item['item_id']};"
                                reddds = con2.execute(del_stmt)
                                if reddds:
                                    con.execute(f"DELETE FROM deleteds WHERE id = {del_item['id']};")
                                    print("deleted", del_item['id'])
                            except:
                                print("item not found")
                                                
                        avilable = 0

                        for table_name in TABLES:
                            statement = f"SELECT id FROM {table_name} WHERE upt = 1"
                            
                            items = con.execute(statement).all()

                            avilable = avilable + len(items)


                        
                        if avilable > 0:

                            soon = 0
                            
                            for table_name in TABLES:

                                statement = f"SELECT * FROM {table_name} WHERE upt = 1"

                                try:
                                
                                    items = con.execute(statement)



                                    
                                    cols = con2.execute(f"SHOW COLUMNS FROM {table_name};")

                                    cols_array = []
                                    for c in cols:  cols_array.append(c[0])
                                    cols_len = len(cols_array)
                                    for item in items:

                                        
                                        stmt1 = f"UPDATE {table_name} SET"
                                        stmt2 = f"INSERT INTO {table_name} ("
                                        stmt2_b = 'VALUES ('

                                        i = 0

                                        for col_name in cols_array:

                                            
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

                                            i += 1

                                        stmt2 = stmt2 + stmt2_b
                                        
                                        statement2 = f"SELECT id FROM {table_name} WHERE id = {item['id']}"
                                        item_yes = con2.execute(statement2).first()
                                        
                                        if item_yes:
                                            result = con2.execute(stmt1)
                                            # print(stmt1)
                                        else:
                                            result = con2.execute(stmt2)
                                            # print(stmt2)

                                        if result:
                                            con.execute(f"UPDATE {table_name} SET upt = 0 WHERE id = {item['id']}")
                                            soon = soon + 1
                                    print("effective", soon)
                                except Exception as e:
                                    print(e)
                    
                    except Exception as e:
                        print(e)

    sc.enter(5, 1, run_db_code, (sc,))



    

if __name__ == "__main__":
    
    s.enter(5, 1, run_db_code, (s,))
    s.run()




        




    

        







