![test](https://github.com/ks6088ts/edge-python/workflows/test/badge.svg)

# edge-python

deploy codes to edge devices written in Python

# Install

```bash
make install
```

# CLI

## read sensors

```bash
poetry run python main.py --help

# record
poetry run python main.py \
  --dt 0.1 \
  --name mock >> record.csv
```

## run servers

```bash
poetry run python server.py --help

# serve
poetry run python server.py \
  --host localhost \
  --port 8080 \
  --dt 0.1
# client app: https://ks6088ts.github.io/quat-viz-ts/
```
