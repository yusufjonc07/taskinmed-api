from sqlalchemy.orm import Session
from app.db import ActiveSession, engine
from sqlalchemy import inspect
from fastapi import APIRouter

gii_router = APIRouter()

@gii_router.get("/generate_full_project_at")
async def get_home(db: Session = ActiveSession):

    inspector = inspect(engine)


    # Beginning of Routes binding generation part
    route_bind_content=""
    route_bind_content = route_bind_content + f"\nfrom fastapi import APIRouter, Depends"
    route_bind_content = route_bind_content + f"\nfrom app.auth import get_current_active_user"
    
    table_names = ['illness', 'illness_comment']

    for table_name in table_names:
        route_bind_content = route_bind_content + f"\nfrom routers.{table_name} import {table_name}_router"


    route_bind_content = route_bind_content + f"\n\nActiveUser = Depends(get_current_active_user)"
    route_bind_content = route_bind_content + f"\nroutes = APIRouter(dependencies=[ActiveUser])\n\n"
    
    # ./ Beginning of Routes binding generation part

    # table_names = engine.table_names()

    for table_name in table_names:

        model_class_name = f"{table_name}".title()


        # Beginning of Model generation part
        model_content = ""
        model_content = "\nfrom datetime import datetime \n"
        model_content = model_content + "from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, DateTime, Time, Text, Boolean \n" 
        model_content = model_content + "from sqlalchemy.orm import relationship \n" 
        model_content = model_content + "from app.db import Base \n \n" 
        model_content = model_content + "now_sanavaqt = datetime.now() \n" 

        model_content = model_content + "\n\nclass"
        model_content = model_content + f" {model_class_name}(Base):\n"
        model_content = model_content + f'    __tablename__ = "{table_name}"\n'
        # ./ Beginning of Model generation part
        
        # Beginning of Schema generation part
        schema_content=""
        schema_content = f"\nfrom typing import Optional\n"
        schema_content = schema_content + f"from fastapi import UploadFile\n"
        schema_content = schema_content + f"from pydantic import BaseModel\n"
        schema_content = schema_content + f"\n\nclass New{model_class_name}(BaseModel):\n"
        # ./ Beginning of Schema generation part


        # Beginning of CRUD functions generation part
        crud_content = ""
        crud_content= crud_content + "\nfrom fastapi import HTTPException"
        crud_content = crud_content + f"\nfrom app.models.{table_name} import {model_class_name}"
        create_of_crud = f"\n\n\ndef create_{table_name}(req, form_data, usr, db):"
        create_of_crud = create_of_crud + f"\n\n    new_{table_name} = {model_class_name}("


        read_of_crud = f"\n\n\ndef read_{table_name}(id, usr, db):"
        read_of_crud = read_of_crud + f"\n\n    this_{table_name} = db.query({model_class_name}).filter({model_class_name}.id == id).first()"
        read_of_crud = read_of_crud + f"\n\n    if this_{table_name}:"
        read_of_crud = read_of_crud + f"\n        return this_{table_name}"
        read_of_crud = read_of_crud + f"\n    else:"
        read_of_crud = read_of_crud + f"\n        raise HTTPException(status_code=400, detail=\"{model_class_name} was not found!\")"
        
        get_all_data = f"\n\n\ndef get_all_{table_name}s(page, limit, usr, db):"
        get_all_data = get_all_data + f"\n\n    if page == 1 or page < 1:"
        get_all_data = get_all_data + f"\n        offset = 0"
        get_all_data = get_all_data + f"\n    else:"
        get_all_data = get_all_data + f"\n        offset = (page-1) * limit"
        get_all_data = get_all_data + f"\n\n    return db.query({model_class_name}).order_by({model_class_name}.id.desc()).offset(offset).limit(limit).all()"
        
        get_count_of_data = f"\n\n\ndef get_count_{table_name}s(usr, db):"
        get_count_of_data = get_count_of_data + f"\n\n    return db.query({model_class_name}).count()"
        

        delete_of_crud = f"\n\n\ndef delete_{table_name}(id, usr, db):"
        delete_of_crud = delete_of_crud + f"\n\n    this_{table_name} = db.query({model_class_name}).filter({model_class_name}.id == id)"
        delete_of_crud = delete_of_crud + f"\n\n    if this_{table_name}.first():"
        delete_of_crud = delete_of_crud + f"\n        this_{table_name}.delete()"
        delete_of_crud = delete_of_crud + f"\n\n        db.commit()"
        delete_of_crud = delete_of_crud + f"\n        return 'This item has been deleted!'"
        delete_of_crud = delete_of_crud + f"\n    else:"
        delete_of_crud = delete_of_crud + f"\n        raise HTTPException(status_code=400, detail=\"{model_class_name} was not found!\")"
       

        update_of_crud = f"\n\n\ndef update_{table_name}(req, id, form_data, usr, db):"
        update_of_crud = update_of_crud + f"\n\n    this_{table_name} = db.query({model_class_name}).filter({model_class_name}.id == id)"
        update_of_crud = update_of_crud + f"\n\n    if this_{table_name}.first():"
        update_of_crud = update_of_crud + f"\n        this_{table_name}.update("+"{"
        # ./ Beginning of CRUD functions generation part


        # Beginning of ROUTER functions generation part
        router_content = ""
        router_content= router_content + "\nfrom fastapi import Depends, APIRouter, HTTPException"
        router_content= router_content + "\nfrom fastapi import HTTPException"
        router_content= router_content + "\nfrom app.db import ActiveSession"
        router_content= router_content + "\nfrom sqlalchemy.orm import Session"
        router_content= router_content + "\nfrom app.auth import get_current_active_user"
        router_content= router_content + "\nfrom app.settings import UserSchema"
        router_content= router_content + f"\nfrom app.functions.{table_name} import *"
        router_content = router_content + f"\nfrom app.models.{table_name} import *"
        router_content = router_content + f"\nfrom app.schemas.{table_name} import *"
        router_content = router_content + f"\n\n{table_name}_router = APIRouter(tags=['{model_class_name} Endpoint'])"
        
        get_of_router = f'\n\n\n@{table_name}_router.get("/{table_name}s", description="This router returns list of the {table_name}s using pagination")'
        get_of_router = get_of_router + f"\nasync def get_{table_name}s_list("
        get_of_router = get_of_router + "\n    page: int = 1,"
        get_of_router = get_of_router + "\n    limit: int = 10,"
        get_of_router = get_of_router + "\n    db:Session = ActiveSession,"
        get_of_router = get_of_router + "\n    usr: UserSchema = Depends(get_current_active_user)\n):"
        get_of_router = get_of_router + "\n    if not usr.role in ['any_role']:"
        get_of_router = get_of_router + f"\n        return get_all_{table_name}s(page, limit, usr, db)"
        get_of_router = get_of_router + "\n    else:"
        get_of_router = get_of_router + '\n        raise HTTPException(status_code=400, detail="Access denided!")'
        
        create_of_router = f'\n\n\n@{table_name}_router.post("/{table_name}/create", description="This router is able to add new {table_name} and return {table_name} id")'
        create_of_router = create_of_router + f"\nasync def create_new_{table_name}("
        create_of_router = create_of_router + f"\n    form_data: New{model_class_name},"
        create_of_router = create_of_router + "\n    db:Session = ActiveSession,"
        create_of_router = create_of_router + "\n    usr: UserSchema = Depends(get_current_active_user)\n):"
        create_of_router = create_of_router + "\n    if not usr.role in ['any_role']:"
        create_of_router = create_of_router + f"\n        return create_{table_name}(req, form_data, usr, db)"
        create_of_router = create_of_router + "\n    else:"
        create_of_router = create_of_router + '\n        raise HTTPException(status_code=400, detail="Access denided!")'


        update_of_router = f'\n\n\n@{table_name}_router.put("/{table_name}/'+'{id}'+f'/update", description="This router is able to update {table_name}")'
        update_of_router = update_of_router + f"\nasync def update_one_{table_name}("
        update_of_router = update_of_router + "\n    id: int,"
        update_of_router = update_of_router + f"\n    form_data: New{model_class_name},"
        update_of_router = update_of_router + "\n    db:Session = ActiveSession,"
        update_of_router = update_of_router + "\n    usr: UserSchema = Depends(get_current_active_user)\n):"
        update_of_router = update_of_router + "\n    if not usr.role in ['any_role']:"
        update_of_router = update_of_router + f"\n        return update_{table_name}(req, id, form_data, usr, db)"
        update_of_router = update_of_router + "\n    else:"
        update_of_router = update_of_router + '\n        raise HTTPException(status_code=400, detail="Access denided!")'
        # ./ Beginning of ROUTER functions generation part

      
        relates = ''
        relates_sources = f"\n"

        for column in inspector.get_columns(table_name, schema='klinika'):

            

            if str(column['name']) == 'id':
                one_col_context = f"    id = Column(Integer, primary_key=True, index=True, autoincrement=True)\n"
                one_prop_context = ""
            else:
                

                col_type = 'Integer'

                if str(column['type']) == 'INTEGER' or str(column['type']) == 'SMALLINT':
                    col_type = "Integer"
                    prop_type = 'int'
                    default_val=0
                elif str(column['type']) == 'TEXT':
                    col_type = "Text"
                    prop_type = 'dict'
                    default_val="''"
                elif str(column['type']) == 'DOUBLE':
                    col_type = "Numeric"
                    prop_type = 'float'
                    default_val=0
                elif str(column['type']) == 'DATETIME':
                    col_type = "DateTime"
                    prop_type = 'str'
                    default_val='now_sanavaqt'
                elif str(column['type']) == 'DATE':
                    col_type = "Date"
                    prop_type = 'str'
                    default_val='now_sanavaqt'
                elif str(column['type']) == 'TIME':
                    col_type = "Time"
                    prop_type = 'str'
                    default_val='now_sanavaqt'
                elif str(column['type']) == 'TINYINT':
                    col_type = "Boolean"
                    prop_type = 'bool'
                    default_val='False'
                else: 
                    col_type = "String"
                    prop_type = 'str'
                    default_val="''"

                if str(column['name'])[-3:] == '_id':
                    foreign = f", ForeignKey('{str(column['name'])[:-3]}.id')"
                    relates =  relates + f"\n    {str(column['name'])[:-3]} = relationship('{str(column['name'])[:-3].title()}', backref='{table_name}s')"
                    relates_sources =  relates_sources + f"from app.models.{str(column['name'])[:-3]} import * \n"
                else:
                    foreign = ''
                    

                if str(column['name']).lower() == 'workplace_id':
                    create_of_crud = create_of_crud + f"\n        {str(column['name'])}=usr.workplace_id,"
                    one_prop_context = ''
                elif str(column['name']).lower() in ['created_at', 'updated_at']:
                    one_prop_context = ''
                else:
                    create_of_crud = create_of_crud + f"\n        {str(column['name'])}=form_data.{str(column['name']).lower()},"
                    update_of_crud = update_of_crud + f"\n            {model_class_name}.{str(column['name'])}: form_data.{str(column['name']).lower()},"
                    one_prop_context = f"    {str(column['name']).lower()}: {prop_type}\n"


                one_col_context = f"    {column['name']} = Column({col_type}{foreign}, default={default_val})\n"

            model_content = model_content + one_col_context 
            schema_content = schema_content + one_prop_context
        
        model_content = relates_sources + model_content + relates

        create_of_crud = create_of_crud + "\n    )"
        create_of_crud = create_of_crud + f"\n\n    db.add(new_{table_name})\n\n    db.commit()"
        create_of_crud = create_of_crud + f"\n    return new_{table_name}.id"

        update_of_crud = update_of_crud + "\n        })"
        update_of_crud = update_of_crud + f"\n\n        db.commit()"
        update_of_crud = update_of_crud + f"\n        return 'Success'"
        update_of_crud = update_of_crud + f"\n    else:"
        update_of_crud = update_of_crud + f"\n        raise HTTPException(status_code=400, detail=\"{model_class_name} was not found!\")"

        crud_content = crud_content + get_count_of_data
        crud_content = crud_content + get_all_data
        crud_content = crud_content + read_of_crud
        crud_content = crud_content + create_of_crud
        crud_content = crud_content + update_of_crud
        crud_content = crud_content + delete_of_crud

        router_content = router_content + get_of_router
        router_content = router_content + create_of_router
        router_content = router_content + update_of_router

        route_bind_content = route_bind_content + f"\nroutes.include_router({table_name}_router)"
        


    #     with open(f'./models/{table_name}.py', 'w') as f:
    #         f.write(f'''\
    # {model_content}       
    # ''')

    #     with open(f'./functions/{table_name}.py', 'w') as f:
    #         f.write(f'''\
    # {crud_content}       
    # ''')

    #     with open(f'./schemas/{table_name}.py', 'w') as f:
    #         f.write(f'''\
    # {schema_content}       
    # ''')

    #     with open(f'./routers/{table_name}.py', 'w') as f:
    #         f.write(f'''\
    # {router_content}       
    # ''')

#     with open(f'./routes.py', 'w') as f:
#         f.write(f'''\
# {route_bind_content}       
# ''')


   
   

