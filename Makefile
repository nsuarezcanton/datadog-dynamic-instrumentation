.PHONY: init
init:
	sed -i '' 's/<DD_API_KEY_HERE>/$(DD_API_KEY)/' datadog.env
	sed -i '' 's/<DD_SITE_HERE>/$(DD_SITE)/' datadog.env

.PHONY: up
up:
	nerdctl compose up --build --detach

.PHONY: destroy
destroy:
	nerdctl compose down
	
.PHONY: logs
logs:
	nerdctl compose logs --follow