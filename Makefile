# Customize these paths based on your project structure
MIGRATIONS_DIR = database/migrations
ENV_FILE = .env  # Path to your .env file

# Check if .env file exists and load variables from it, else fallback to env vars
ifneq ("$(wildcard $(ENV_FILE))","")
    include $(ENV_FILE)
    export $(shell sed 's/=.*//' $(ENV_FILE))
else
    $(info No $(ENV_FILE) file found, using shell environment variables)
endif

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

test-ddos-should-error-with-429:
	@flask test-ddos-should-error-with-429 \
		$(if $(url),--url $(url),) \
		$(if $(request-count),--request-count $(request-count),) \
		$(if $(thread-count),--thread-count $(thread-count),)
	
generate-secret-key:
	@flask generate-secret-key --env-file $(ENV_FILE)

scrap-price-histories-then-insert:
	@flask scrap-price-histories-then-insert

.PHONY: db-init db-migrate db-upgrade db-downgrade db-history db-fresh db-seed db-fresh-seed generate-secret-key scrap-price-histories-then-insert
