# cc-summariser #

`cc-summariser` creates a summary of [compliance-checker](https://github.com/ioos/compliance-checker)
results from running checks on multiple datasets.

## Installation ##

```
git clone https://github.com/cedadev/cc-summariser
pip install ./cc-summariser

# Multiple dataset output is not yet on master branch...
pip install git+https://github.com/ioos/compliance-checker@refactor-scoring
```

## Usage ##

The most basic usage is as follows:
```
compliance-checker -f json_new -o results.json --test <your test(s)> <dataset>...
cc-summariser results.json
```

For more options see the output of `cc-summariser --help`:
```
usage: cc-summariser [-h] [-l FILE_LIMIT] [-f {text,json}] results_file

Summarise the results compliance-checker run on multiple datasets

positional arguments:
  results_file          File containing compliance-checker results in
                        'json_new' format

optional arguments:
  -h, --help            show this help message and exit
  -l FILE_LIMIT, --file-limit FILE_LIMIT
                        The maximum number of offending files to list in the
                        'Failure details' section in the text format output
  -f {text,json}, --format {text,json}
                        Format to print summary in
```

## Output ##

The default format if not specified with `--format` is `text`.

### JSON ###

JSON output is of the following form:
```
{
    "num_files": <total files checked>,
    "num_no_errors": <number of files with no check failures>,
    "summary": {
        "high_priorities": {
            <checker name>: [
                {
                    "name": <check name>,
                    "count": <number of files that failed this check>,
                    "files": [<file 1>, <file 2>, ...],
                    "msgs": [
                        {
                            "msg": <msg 1>,
                            "count": <n>,
                            "files": <files with this failure message>
                        },
                        ...
                    ]
                },
                ...
            ],
            ...
        },
        "medium_priorities": {...},
        "low_priorities": {...}
    }
}
```

### Text ###

The text output contains the same information as the JSON format but in a more
human-readable layout. It is split into two sections

- The 'Failures summary' section lists only the number of files that failed
  each check. This section is easy to scan through to see where checks are
  failing the most.

- The 'Failure details' section lists the filenames that failed each check and
  reasons for the check failing (if available).

  The `--file-limit` command line option limits the number of filenames listed
  here; e.g. if 10 files failed a check and `--file-limit=4` the output would
  be

  ```
  file_1.nc
  file_2.nc
  ...
  file_9.nc
  file_10.nc
  ```
