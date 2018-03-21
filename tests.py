import pytest

from cc_summarizer import (get_summary_dict, indent, pluralise, underline, truncate_list,
                           remove_empty_values)


class TestSummarizer(object):
    def test_single_file(self):
        summarized = get_summary_dict({
            "file.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"], "value": [4, 5]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        assert "num_files" in summarized and summarized["num_files"] == 1
        assert "num_no_errors" in summarized and summarized["num_no_errors"] == 0
        assert "summary" in summarized

        for level in ("high", "medium", "low"):
            level_name = "{}_priorities".format(level)
            assert level_name in summarized["summary"]
            assert "check_name" in summarized["summary"][level_name]

        assert summarized["summary"]["high_priorities"]["check_name"] == [{
            "name": "high p error",
            "msgs": [{"msg": "h", "count": 1, "files": ["file.nc"]}],
            "files": ["file.nc"],
            "count": 1
        }]

    def test_multiple_files(self):
        summarized = get_summary_dict({
            "file1.nc": {
                "check_name": {
                    "high_priorities": [
                        {"name": "high p error", "msgs": ["h1", "h2"], "value": [4, 5]}
                    ],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            },
            "file2.nc": {
                "check_name": {
                    "high_priorities": [
                        {"name": "high p error", "msgs": ["h1", "h3"], "value": [4, 5]},
                    ],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        assert len(summarized["summary"]["high_priorities"]["check_name"]) == 1
        high_p = summarized["summary"]["high_priorities"]["check_name"][0]

        assert high_p["name"] == "high p error"

        expected_msgs = [
            {"msg": "h1", "count": 2, "files": ["file1.nc", "file2.nc"]},
            {"msg": "h2", "count": 1, "files": ["file1.nc"]},
            {"msg": "h3", "count": 1, "files": ["file2.nc"]}
        ]
        for m in expected_msgs:
            assert m in high_p["msgs"]
        for m in high_p["msgs"]:
            assert m in expected_msgs

        assert high_p["files"] == ["file1.nc", "file2.nc"]
        assert high_p["count"] == 2

    def test_no_errors(self):
        summarized = get_summary_dict({
            "with_errors.nc": {
                "mycheck": {
                    "high_priorities": [
                        {"name": "error", "msgs": ["e"], "value": [4, 5]},
                        {"name": "not error", "msgs": ["e"], "value": [5, 5]}
                    ],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            },
            "no_errors.nc": {
                "mycheck": {
                    "high_priorities": [
                        {"name": "not error", "msgs": ["e"], "value": [5, 5]}
                    ],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        # no_errors.nc should have no errors
        assert summarized["num_no_errors"] == 1
        # Checks with full score should not be included
        assert len(summarized["summary"]["high_priorities"]["mycheck"]) == 1


class TestMiscFunctions(object):
    def test_indent(self):
        assert indent("hello\nthere", level=2) == "        hello\n        there"

    def test_underline(self):
        assert underline("some text", "@") == "some text\n@@@@@@@@@"

    def test_remove_empty_values(self):
        assert remove_empty_values({"key": "value"}) == {"key": "value"}
        assert remove_empty_values({"key": []}) == {}
        d = {"key": {"high": [], "medium": ["yes"], "low": None}}
        assert remove_empty_values(d) == {"key": {"medium": ["yes"]}}

    def test_pluralise(self):
        assert pluralise("house", 2) == "houses"
        assert pluralise("house", 1) == "house"

    def test_trunacte_list(self):
        assert truncate_list([1, 2, 3], 5) == [1, 2, 3]
        assert truncate_list([1, 2, 3], 1) == ["...", 3]
        assert truncate_list([1, 2, 3, 4, 5, 6], 3) == [1, "...", 5, 6]
        assert truncate_list([1, 2, 3, 4, 5, 6], 4) == [1, 2, "...", 5, 6]
