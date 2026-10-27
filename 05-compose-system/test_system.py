"""End-to-end test of the running system: status codes, answers and the log."""
import mimetypes
import sys

import requests

BASE_URL = "http://localhost:8701"
BIG = "<6 MB generated jpeg>"  # real JPEG padded in memory past 5 MB, sent as image/jpeg -> 413
CASES = [  # (image, question, expected status)
    ("samples/coco_000000039769.jpg", "How many cats are there?", 200),
    ("samples/coco_000000039769.jpg", "What color is the couch?", 200),
    ("samples/coco_000000000139.jpg", "What room is this?", 200),
    ("samples/coco_000000000139.jpg", "Is there a TV?", 200),
    ("samples/coco_000000000632.jpg", "What is the main furniture?", 200),
    ("samples/coco_000000000632.jpg", "Is there a bookshelf?", 200),
    ("samples/coco_000000039769.jpg", "", 422),
    ("samples/not_an_image.txt", "What is this?", 400),
    (BIG, "What is this?", 413),
    ("samples/coco_000000039769.jpg", "cat " * 100, 500),
]

# Send each case and compare the status code with the expected one
passed = 0
for path, question, expected in CASES:
    with open("samples/coco_000000039769.jpg" if path == BIG else path, "rb") as f:
        data = f.read().ljust(6 * 1024 * 1024 + 1 if path == BIG else 0, b"\0")
    resp = requests.post(f"{BASE_URL}/predict", data={"question": question}, timeout=60,
                         files={"image": (path, data, mimetypes.guess_type(f.name)[0])})
    ok = resp.status_code == expected
    passed += ok
    body = resp.json()
    print(resp.status_code, "PASS" if ok else "FAIL", path, repr(question[:30]),
          "->", body.get("answer", body.get("detail")))

# Show what the API wrote to its SQLite log, then the summary
print("\nGET /logs:")
for row in requests.get(f"{BASE_URL}/logs", timeout=10).json():
    print(row)
print(f"\n{passed}/{len(CASES)} passed")
sys.exit(1 if passed < len(CASES) else 0)
