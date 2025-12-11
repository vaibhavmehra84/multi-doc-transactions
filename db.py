from motor.motor_asyncio import AsyncIOMotorClient

#MONGO_URI = "mongodb+srv://someurl/"
MONGO_URI = "mongodb://localhost:27017/?directConnection=true"

client = AsyncIOMotorClient(MONGO_URI)
db = client.payment_system

wallets = db.wallets
ledger = db.ledger_entries
idem = db.idempotency
