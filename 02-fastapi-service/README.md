# Part 02 - FastAPI service

ViLT VQA served with FastAPI (router / service / model registry, model loaded once in `lifespan`).

```bash
pip install -r requirements.txt
uvicorn app.main:app --port 8701   # terminal 1
python client.py                   # terminal 2
```

Interactive docs: http://localhost:8701/docs

| Status | When |
|--------|------|
| 200 | Answer returned |
| 400 | Not a JPEG/PNG, or bytes are not a valid image |
| 413 | Image larger than 5 MB |
| 422 | Question empty, or a form field is missing |
| 500 | Inference failed (e.g. question longer than 40 tokens) |
| 503 | Model is not loaded |

For the 413 curl demo (`-F image=@samples/big_image.jpg`), first create the file (about 7 MB, git-ignored):
`python -c "from PIL import Image; Image.open('samples/coco_000000039769.jpg').resize((4800, 3600)).save('samples/big_image.jpg', quality=100)"`
