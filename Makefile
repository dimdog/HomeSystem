ACTIVATE = $(PWD)/activate
PREFIX = $(PWD)/venv/bin/
PIP_CACHE = $(PWD)/venv/
PIP_TIMEOUT = 100
PIP_OPTS = -i http://pypi.python.org/simple --timeout=$(PIP_TIMEOUT) --download-cache=$(PIP_CACHE)
PIP_INSTALL = . $(ACTIVATE) && $(PREFIX)pip install $(PIP_OPTS)
.PHONY : _install update

update: 
	$(PIP_INSTALL) --requirement=requirements.txt 

install : _install update

_install : 
	sudo apt-get update
	sudo apt-get install python-virtualenv python-dev -y
	test -d $(PWD)/venv || virtualenv venv

prod : _prod update prod.cfg

_prod :
	test -d $(PWD)/venv || virtualenv venv
	mkdir -p logs
      
clean:
	pip uninstall -y -r requirements.txt
	find . -type f -name "*.pyc" -exec rm {} \;

%.cfg:
	ln -sf $(PWD)/config/$@ config/active.cfg
