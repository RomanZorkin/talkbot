include .env
export

run:
	@python -m bot


lint:
	@flake8 bot
	@mypy bot