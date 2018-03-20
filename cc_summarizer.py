"""
things to check with this approach:
- what is 'children' in each result dict?
"""
from __future__ import unicode_literals, print_function
import codecs
import sys
import io
import json
from collections import OrderedDict

__version__ = "0.0.1"

# Ensure output is encoded as Unicode when output is redirected or piped
if sys.stdout.encoding is None:
    sys.stdout = codecs.getwriter("utf8")(sys.stdout)
if sys.stderr.encoding is None:
    sys.stderr = codecs.getwriter("utf8")(sys.stderr)

PRIORITY_LEVELS = ["high_priorities", "medium_priorities", "low_priorities"]


def indent(text, level):
    """
    Indent each line in a string by prepending whitespace
    """
    return "\n".join([" " * (2 * level) + line for line in text.split("\n")])


def underline(text, underline_char):
    """
    Underline `text` by adding a new line and `underline_chars`
    """
    return text + "\n" + (underline_char * len(text))


def pluralise(word, n):
    return word + "s" if n > 1 else word


def remove_empty_values(d):
    """
    Recursively iterate over a dictionary and remove keys whose value is Falsy
    (empty list, empty dict, None etc)
    """
    new_d = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = remove_empty_values(v)

        if v:
            new_d[k] = v
    return new_d


def brief_text(res_dict):
    """
    Return a string to be included in the brief summary section of the text
    report
    """
    files_str = pluralise("file", res_dict["count"])
    return "- {name}: {count} {}".format(files_str, **res_dict)


def detailed_text(res_dict):
    """
    Return a string to be included in the detailed section of the text
    """
    files_str = pluralise("file", res_dict["count"])
    lines = ["- {name}: ({count} {})".format(files_str, **res_dict)]
    for filename in sorted(res_dict["files"]):
        lines.append(indent(filename, level=1))
    lines.append("")

    return "\n".join(lines)


def get_summary_text(summary_dict):
    """
    Return a human readable text version of summary information from the dict
    format produced by get_summary_dict
    """
    lines = []
    lines.append("File scanned: {num_files}".format(**summary_dict))
    lines.append("Number of files with no errors: {num_no_errors}"
                 .format(**summary_dict))
    lines.append("")

    summary = summary_dict["summary"]
    sections = [
        ("Failures summary", brief_text),
        ("Failure details", detailed_text)
    ]
    for section_name, callback in sections:
        lines.append(underline(section_name, "="))
        lines.append("")
        for p_level in summary:
            # Format priority level in a more readable way
            p_level_name = p_level.replace("_priorities", "").upper()
            lines.append(underline("{}:".format(p_level_name), "-"))

            for check_name in summary[p_level]:
                lines.append(indent("- {}:".format(check_name), level=1))

                for res in summary[p_level][check_name]:
                    lines.append(indent(callback(res), level=2))
                lines.append("")

    return "\n".join(lines).strip()


def get_summary_dict(dict_output):
    """
    Summarize compliance-checker results in 'json_new' format from checks on
    several datasets, and return a dict of the form
    {
        "num_files": "<number of files tested>",
        "num_no_errors": "<number of files without any errors">,
        "summary": {
            "high_priorities": {
                "<check one>": [
                    {
                        "name": "<failure name>",
                        "msgs": ["<failure message>", ...],
                        "count": <number of files that failed the check>,
                        "files": [<filename>, ...]
                    },
                    ...
                ],
                ...
            },
            ...
        }
    }
    """
    files_with_errors = set([])

    summary = OrderedDict()
    for p_level in PRIORITY_LEVELS:
        summary[p_level] = {}

    for filename, checks in dict_output.items():
        for check_name, result_dict in checks.items():
            for p_level in PRIORITY_LEVELS:
                if check_name not in summary[p_level]:
                    summary[p_level][check_name] = []

                for res in result_dict[p_level]:
                    # Skip if there is no error for this check
                    score, out_of = res["value"]
                    if score == out_of:
                        continue

                    files_with_errors.add(filename)
                    # Find existing error with this name, or create new
                    # entry
                    summarized_info = None
                    for s in summary[p_level][check_name]:
                        if s["name"] == res["name"]:
                            summarized_info = s
                            break
                    else:
                        summarized_info = {"name": res["name"], "count": 0,
                                           "files": [], "msgs": []}
                        summary[p_level][check_name].append(summarized_info)

                    summarized_info["count"] += 1
                    summarized_info["files"].append(filename)
                    for msg in res["msgs"]:
                        if msg not in summarized_info["msgs"]:
                            summarized_info["msgs"].append(msg)

    return {
        "num_files": len(dict_output),
        "num_no_errors": len(dict_output) - len(files_with_errors),
        "summary": remove_empty_values(summary)
    }


def usage():
    print("Usage: cc-summarizer RESULTS", file=sys.stderr)


def main():
    if len(sys.argv) != 2:
        usage()
        return 1

    with io.open(sys.argv[1], encoding="utf-8") as f:
        input_results = json.load(f)

    summary = get_summary_text(get_summary_dict(input_results))
    print(summary)
    return 0


if __name__ == "__main__":
    status = main()
    # python 2 prints an error message if stdout has not been fully read when
    # python exits (e.g. when piping output to 'head'), so flush and ignore
    # errors
    try:
        sys.stdout.flush()
    except IOError:
        pass

    sys.exit(status)