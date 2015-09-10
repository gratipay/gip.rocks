env:
	virtualenv env --prompt="[gip]"

run: env
	run_dammit defaults.env web
