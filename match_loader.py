import pandas as pd
from supabase import create_client, Client

# 1. Initialize Supabase Client
SUPABASE_URL = ""
SUPABASE_KEY = "" #removed for safety

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Read the CSV file
file_path = "Toss - Sheet1.csv"
df = pd.read_csv(file_path)

# 3. Clean and rename columns to match Supabase schema exactly
# Renaming 'match_id' -> 'matchid' and fixing the 'battting_first' typo
df = df.rename(columns={
    'match_id': 'matchid',
    'battting_first': 'batting_first'
})


df['matchid'] = df['matchid'].astype(str)

df = df.where(pd.notnull(df), None)

records = df.to_dict(orient="records")

# 4. Insert data into Supabase in batches 

batch_size = 1000
total_inserted = 0

print(f"Starting insertion of {len(records)} rows...")

for i in range(0, len(records), batch_size):
    batch = records[i:i + batch_size]
    
    # Perform the insert
    data, count = supabase.table("apl_win_info").insert(batch).execute()
    
    total_inserted += len(batch)
    print(f"Inserted {total_inserted} / {len(records)} rows...")

print("Data insertion complete!")