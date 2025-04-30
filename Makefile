# Customize these paths based on your project structure
MIGRATIONS_DIR = database/migrations
ENV_FILE = .env  # Path to your .env file

# Load environment variables from .env file
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

# Initialize migrations directory
db-init:
	@flask db init --directory $(MIGRATIONS_DIR)

# Generate a new migration
db-migrate:
	@flask db migrate --directory $(MIGRATIONS_DIR) -m "$(m)"

# Apply migrations
db-upgrade:
	@flask db upgrade --directory $(MIGRATIONS_DIR)

# Revert migrations
db-downgrade:
	@flask db downgrade base --directory $(MIGRATIONS_DIR)

# Show migration history
db-history:
	@flask db history --directory $(MIGRATIONS_DIR)

db-fresh:
	$(MAKE) db-downgrade
	$(MAKE) db-upgrade

db-seed: 
	@flask db-seed

db-fresh-seed:
	$(MAKE) db-fresh
	$(MAKE) db-seed
	
generate-secret-key:
	@flask generate-secret-key --env-file $(ENV_FILE)

.PHONY: db-init db-migrate db-upgrade db-downgrade db-history db-fresh db-seed db-fresh-seed generate-secret-key
