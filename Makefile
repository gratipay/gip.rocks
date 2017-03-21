env:
	python -m virtualenv --python=python2.7 env --prompt="[gip]"
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env

run: env
	bin/run defaults.env web
