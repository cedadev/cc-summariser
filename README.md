# cc-summarizer #

`cc-summarizer` creates a summary of [compliance-checker](https://github.com/ioos/compliance-checker)
results from running checks on multiple datasets.

## Installation ##

```
git clone https://github.com/joesingo/cc-summarizer
pip install ./cc-summarizer

# Multiple dataset output is not yet on master branch...
pip install git+https://github.com/ioos/compliance-checker@refactor-scoring
```

## Usage ##
```
compliance-checker -f json_new -o results.json --test <your test(s)> <dataset>...
cc-summarizer results.json summarized.json
```
