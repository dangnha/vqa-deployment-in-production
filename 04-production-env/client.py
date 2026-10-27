"""Demo client: call the VQA service with valid and invalid requests."""
import requests

BASE_URL = "http://localhost:8701"
IMAGE = "samples/coco_000000039769.jpg"


def show(title, response):
    print(f"--- {title} -> {response.status_code}")
    print(response.json())


def big_jpeg():
    # A real JPEG padded in memory to just over 6 MB (limit is 5 MB): sent as
    # image/jpeg it passes the type check and gets 413 from the size check
    with open(IMAGE, "rb") as f:
        return f.read().ljust(6 * 1024 * 1024 + 1, b"\0")


def predict(question=None, path=IMAGE, mime="image/jpeg", content=None):
    # Send the file (or the given bytes) as multipart; add the question only if given
    data = {} if question is None else {"question": question}
    if content is None:
        with open(path, "rb") as f:
            content = f.read()
    files = {"image": (path, content, mime)}
    return requests.post(f"{BASE_URL}/predict", files=files, data=data)


show("(a) health", requests.get(f"{BASE_URL}/health"))
show("(b) valid question", predict("How many cats are there?"))
show("(c) empty question", predict("   "))
show("(d) missing question", predict())
show("(e) not an image", predict("What is this?", "samples/not_an_image.txt", "text/plain"))
show("(f) question too long", predict("what color is the cat " * 20))
show("(g) image too big", predict("What is this?", "<6 MB generated jpeg>", content=big_jpeg()))
