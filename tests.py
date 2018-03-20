import pytest

from cc_summarizer import get_summary_dict


class TestSummariser(object):
    def test_single_file(self):
        summarized = get_summary_dict({
            "file.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"],
                                         "value": [4, 5]}],
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
            "name": "high p error", "msgs": ["h"], "files": ["file.nc"],
            "count": 1
        }]

    def test_multiple_files(self):
        summarized = get_summary_dict({
            "file1.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"],
                                         "value": [4, 5]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            },
            "file2.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"],
                                         "value": [4, 5]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        assert len(summarized["summary"]["high_priorities"]["check_name"]) == 1
        high_p = summarized["summary"]["high_priorities"]["check_name"][0]
        assert high_p["name"] == "high p error"
        assert high_p["msgs"] == ["h"]
        assert set(high_p["files"]) == set(["file1.nc", "file2.nc"])
        assert high_p["count"] == 2
