"""Demo client: call the VQA service with valid and invalid requests."""
import requests

BASE_URL = "http://localhost:8701"
IMAGE = "samples/coco_000000039769.jpg"


def show(title, response):
    print(f"--- {title} -> {response.status_code}")
    print(response.json())


def predict(question=None, path=IMAGE, mime="image/jpeg"):
    # Send the file as multipart; add the question field only if given
    data = {} if question is None else {"question": question}
    with open(path, "rb") as f:
        files = {"image": (path, f, mime)}
        return requests.post(f"{BASE_URL}/predict", files=files, data=data)


show("(a) health", requests.get(f"{BASE_URL}/health"))
show("(b) valid question", predict("How many cats are there?"))
show("(c) empty question", predict("   "))
show("(d) missing question", predict())
show("(e) not an image", predict("What is this?", "samples/not_an_image.txt", "text/plain"))
show("(f) question too long", predict("what color is the cat " * 20))
