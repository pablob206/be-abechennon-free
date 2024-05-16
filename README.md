# be-abechennon-free
## Backend - Api RESTFul

### Initialize environment:
```bash
python3 -m venv venv
source venv/bin/activate
touch .env  # build .env/copy .env.sample
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -r requirements_test.txt

# Python: clear cache and reload window (VsCode)
ctrl+shift+p

# Must be set '.env' file.
```

### Install TA-LIB (this is a requirements dependency):
```bash
# https://blog.quantinsti.com/install-ta-lib-python/#windows

sudo apt-get -y install gcc build-essential

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
  && sudo tar -xzf ta-lib-0.4.0-src.tar.gz \
  && sudo rm ta-lib-0.4.0-src.tar.gz \
  && cd ta-lib/ \
  && sudo ./configure --prefix=/usr \
  && sudo make \
  && sudo make install \
  && cd ~ \
  && sudo rm -rf ta-lib/ \
  && pip install ta-lib
```

### Commands utilities:
```bash
# black
black .
# flake8
flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
# pre-commit
pre-commit run --all-files
# bandit
python -m bandit -r test

# pytest
pytest -v
```
