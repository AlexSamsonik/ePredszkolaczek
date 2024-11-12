# ePredszkolaczek
A project to calculate the actual number of hours children are in kindergarten.

- Install Virtual Environment (venv):
```sh
python -m venv venv
```

- Activate venv:
```sh
source venv/bin/activate
```

- Install poetry
```sh
pip install poetry
```

- Install dependencies via poetry
```sh
poetry install
```

- Install pre-commit hooks. (Optional. Only for development)
```sh
pre-commit install
```

- Install playwright
```sh
playwright install
```

- Running script without param (default)
```sh
python ./calculate_presenting_and_hours.py
```

- Running script with param '-m'. Calculate for specific month.
```sh
python ./calculate_presenting_and_hours.py -m 9  # will be calculate for September.
```
