"""
things to check with this approach:
- what is 'children' in each result dict?
"""
import sys
import io
import json


__version__ = "0.0.1"


def summarize(dict_output):
    """
    Summarize the results from checks on several datasets into a JSON
    structure.

    The returned dict is of the form
    {
        <check name>: {
            "high_priorities": [{
                "name": <name>,
                "msgs": [<message>, ...],
                "count": <number of files with this error>,
                "files": [<file 1>, <file 2>, ...]
            }, ...],
            "medium_priorities": [...],
            "low_priorities": [...]
        },
        <check two>: {...}
    }

    @param dict_output    Check results as a dict in the 'json_new' format
    @return               Summarized results as a dict
    """
    summary = {}
    for filename, checks in dict_output.items():
        for check_name, result_dict in checks.items():
            priority_levels = ["high_priorities", "medium_priorities", "low_priorities"]

            # Group by check name first
            if check_name not in summary:
                summary[check_name] = {p_level: [] for p_level in priority_levels}

            for p_level in priority_levels:
                for res in result_dict[p_level]:
                    # Find existing error with this name, or create new
                    # entry
                    summarized_info = None
                    for s in summary[check_name][p_level]:
                        if s["name"] == res["name"]:
                            summarized_info = s
                            break
                    else:
                        summarized_info = {"name": res["name"], "count": 0,
                                           "files": [], "msgs": []}
                        summary[check_name][p_level].append(summarized_info)

                    summarized_info["count"] += 1
                    summarized_info["files"].append(filename)
                    for msg in res["msgs"]:
                        if msg not in summarized_info["msgs"]:
                            summarized_info["msgs"].append(msg)
    return summary


def usage():
    print("Usage: cc-summarizer RESULTS OUTPUT_FILE")


def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    results_filename, output_filename = sys.argv[1:3]

    with io.open(results_filename, encoding="utf-8") as f:
        input_results = json.load(f)

    summarized = summarize(input_results)

    with io.open(output_filename, "w", encoding="utf-8") as f:
        dump = json.dumps(summarized, ensure_ascii=False, indent=4)
        f.write(dump)


if __name__ == "__main__":
    main()
