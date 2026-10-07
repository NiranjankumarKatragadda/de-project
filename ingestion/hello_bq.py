from google.cloud import bigquery

client = bigquery.Client(project="retail-dev-nk2026")
print("Project:", client.project)
rows = client.query("SELECT 'it works' AS msg").result()
for r in rows:
    print(r.msg)