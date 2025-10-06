from pymongo import MongoClient

# Replace with your actual connection string
uri = "mongodb+srv://jobify_admin:Dv330YWjb4N6bwgq@cluster0.jqvomet.mongodb.net/job_portal?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB!")
except Exception as e:
    print("❌ Connection failed:", e)
