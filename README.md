# be-abechennon-free [Backend | Api RESTFul]
Cryptocurrency Margin Trading Bot Project For Binance

### Initialize environment:
```bash
python3 -m venv venv
source venv/bin/activate
touch .env  # Must be set '.env' file (see .env.sample)
pip install -r requirements.txt
pip install -r requirements_dev.txt
pip install -r requirements_test.txt
uvicorn main:app --reload

# Python: clear cache and reload window (VsCode)
ctrl+shift+p

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
