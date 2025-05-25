// Switch to the target database
db = db.getSiblingDB('chartnalyze');

// Check if 'watched_assets' collection exists, and create it if not
if (!db.getCollectionNames().includes('watched_assets'))
    db.createCollection('watched_assets');  // Create collection only if it doesn't exist
