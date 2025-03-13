# ePredszkolaczek
A project to calculate the actual number of hours children are in kindergarten.

Requirement:
 - Installed python version 3.12
 - Installed poetry:
```sh
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Running:

- Install poetry dependencies
```sh
poetry install
```

- Install pre-commit hooks. (Optional. Only for development)
```sh
pre-commit install
```

- Running script without param (default)
```sh
poetry run python ./calculate_presenting_and_hours.py
```

- Running script with param '-m' and '-y'. Calculate for specific month and year.
```sh
poetry run python ./calculate_presenting_and_hours.py -m 2 -y 2025  # will be calculate for March 2025.
```
