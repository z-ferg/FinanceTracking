import sensitive
from supabase import create_client

PROJ_URL = "https://ldqjmpsccofsdmmxdgyf.supabase.co"

def view_table(table, view_limit=25, filter=None):
    supabase = create_client(PROJ_URL, sensitive.service_role_key)
    
    if not filter:
        return supabase.table(table).select("*").limit(view_limit).execute()
    else:
        return supabase.table(table).select().filter(column=filter['col'], operator=filter['op'], criteria=filter['x']).execute()


def add_to_db(table, row_vals):
    supabase = create_client(PROJ_URL, sensitive.service_role_key)
    return supabase.table(table).insert(row_vals).execute()