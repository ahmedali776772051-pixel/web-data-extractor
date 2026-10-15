from app.core.extractor import extract_by_css, fetch_html
import pytest

SAMPLE_HTML = """
<html><body>
  <div class="item"><h2>Title 1</h2><p>Some content</p></div>
  <div class="item"><h2>Title 2</h2><p>Other content</p></div>
</body></html>
"""


def test_extract_by_css():
    results = extract_by_css(SAMPLE_HTML, ".item h2")
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["text"] == "Title 1"
    assert results[1]["text"] == "Title 2"


def test_fetch_html_invalid():
    # This test checks that network errors propagate (may be flaky on some networks).
    with pytest.raises(Exception):
        # non-routable IP with tiny timeout to provoke an error quickly
        fetch_html("http://10.255.255.1", timeout=0.001)
```
