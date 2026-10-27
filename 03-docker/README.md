# Part 03 - Docker

The part 02 ViLT VQA service, packaged as a CPU-only Docker image.

**Layer caching:** the Dockerfile copies `requirements.txt` and runs `pip install`
*before* copying `app/`. Editing code only rebuilds the last layer, so torch is not reinstalled.

**Cache mount:** `HF_HOME=/hf_cache` keeps the model weights (~450 MB) out of the image.
Mount a host folder or a volume there: the first run downloads, the next runs reuse it.

```bash
docker build -t vqa-api:03 .
docker images vqa-api:03          # check the image size
```

Run with a bind mount (host folder `./hf_cache`); `--user` keeps the files owned by you, not root, so no sudo to delete:

```bash
mkdir -p hf_cache
docker run --rm -p 8701:8000 --user "$(id -u):$(id -g)" -v "$(pwd)/hf_cache:/hf_cache" vqa-api:03
```

Or with a named volume managed by Docker:

```bash
docker volume create hf_cache
docker run --rm -p 8701:8000 -v hf_cache:/hf_cache vqa-api:03
```

Start the container a second time and check the log: the model now loads from the cache, no download.

From the host (needs `pip install requests`): `python client.py`. Docs: http://localhost:8701/docs

For the 413 curl demo (`-F image=@samples/big_image.jpg`), first create the file (about 7 MB, git-ignored):
`python -c "from PIL import Image; Image.open('samples/coco_000000039769.jpg').resize((4800, 3600)).save('samples/big_image.jpg', quality=100)"`

## Run without Docker

```bash
pip install -r requirements.txt requests
HF_HOME=./hf_cache uvicorn app.main:app --port 8701
```
