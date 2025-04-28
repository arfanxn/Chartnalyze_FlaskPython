# Customize these paths based on your project structure
MIGRATIONS_DIR = database/migrations
ENV_FILE = .env  # Path to your .env file

# Load environment variables from .env file
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

# Initialize migrations directory
db-init:
	flask db init --directory $(MIGRATIONS_DIR)

# Generate a new migration
db-migrate:
	flask db migrate --directory $(MIGRATIONS_DIR) -m "$(m)"

# Apply migrations
db-upgrade:
	flask db upgrade --directory $(MIGRATIONS_DIR)

# Revert migrations
db-downgrade:
	flask db downgrade --directory $(MIGRATIONS_DIR)

# Show migration history
db-history:
	flask db history --directory $(MIGRATIONS_DIR)
	
#
generate-secret-key:
	python app/clis/generate_secret_key.py --env-file .env

# Run the Flask app (optional)
server:
	flask run

.PHONY: db-init db-migrate db-upgrade db-downgrade db-history generate-secret-key server
