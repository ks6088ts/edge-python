![test](https://github.com/ks6088ts/edge-python/workflows/test/badge.svg)

# edge-python

deploy codes to edge devices written in Python

# Install

```bash
make install
```

# CLI

```bash
# help
poetry run python main.py --help
# record
poetry run python main.py \
  --dt 0.1 \
  --name mock >> record.csv
```
