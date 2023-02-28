include .env
export

run:
	@python -m bot


lint:
	@mypy bot
	@flake8 bot