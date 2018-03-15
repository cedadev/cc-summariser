import pytest

from cc_summarizer import summarize


class TestSummariser(object):
    def test_single_file(self):
        summarized = summarize({
            "file.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        assert "check_name" in summarized
        for level in ("high", "medium", "low"):
            assert "{}_priorities".format(level) in summarized["check_name"]

        assert summarized["check_name"]["high_priorities"] == [{
            "name": "high p error", "msgs": ["h"], "files": ["file.nc"], "count": 1
        }]

    def test_multiple_files(self):
        summarized = summarize({
            "file1.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            },
            "file2.nc": {
                "check_name": {
                    "high_priorities": [{"name": "high p error", "msgs": ["h"]}],
                    "medium_priorities": [],
                    "low_priorities": []
                }
            }
        })

        assert len(summarized["check_name"]["high_priorities"]) == 1
        high_p = summarized["check_name"]["high_priorities"][0]
        assert high_p["name"] == "high p error"
        assert high_p["msgs"] == ["h"]
        assert set(high_p["files"]) == set(["file1.nc", "file2.nc"])
        assert high_p["count"] == 2
