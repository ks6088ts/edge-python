# 作業ログ

```bash
# initialize a project with poetry
poetry init
# install dev dependencies
poetry add --dev black pylint pytest
# generate rcfile template
poetry run pylint --generate-rcfile > .pylintrc

# run scripts
python main.py -h
python main.py

# check ci
make ci
```
