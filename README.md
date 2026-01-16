# Doorbell Compliment Service

A Jetson-powered web service that analyzes doorbell images, analyzes the visitor's appearance, then returns a personalized compliment.

This project runs on **NVIDIA Jetson Orin Nano** using [jetson-containers](https://github.com/dusty-nv/jetson-containers) and `l4t-pytorch`, providing a lightweight FastAPI endpoint to handle incoming images and generate compliments (or descriptions) of visitors.

## Features

* FastAPI web server at `/doorbell`
* GPU-accelerated image analysis with PyTorch / TorchVision
* Compatible with JetPack 6 / L4T 36.x
* Easy containerized workflow with jetson-containers

## Prerequisites

* NVIDIA Jetson Orin Nano Developer Kit
* JetPack 6 / L4T 36.x installed
* `jetson-containers` installed on the host
* Python 3.10+ (via container)

---

## Running the Project

### Using jetson-containers (recommended)

From the host:

```bash
cd ~/source/jetson-containers
jetson-containers run \
  -v ~/projects/doorbell_compliment_service:/workspace/doorbell_compliment_service \
  $(autotag l4t-pytorch)
```

Once in the container's interactive prompt, run the server.

```bash
cd /workspace/doorbell_compliment_service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

## Using a custom Docker image (production)

Build with BuildKit enabled to speed up image builds.

```bash
DOCKER_BUILDKIT=1 docker build --progress=plain -t doorbell-compliment .
```

Run with custom mappings for homeassitant using the LAN address.

```bash
docker run -d \
  --name doorbell-compliment \
  --restart unless-stopped \
  --runtime nvidia \
  --network host \
  --add-host homeassistant.local:192.168.1.93 \
  -v $(pwd):/app \
  doorbell-compliment
```

The server will start on `localhost:8080`.

## Testing the Doorbell Endpoint

```bash
curl http://localhost:8080/doorbell
```

Expected output (example):

```json
{
  "description": "I see a visitor who looks absolutely wonderful today."
}
```

---

## Development Tips

* Edit the code directly in VS Code via [Remote – SSH](https://code.visualstudio.com/docs/remote/ssh)
* Mount your repo to the container for hot edits
* Cache Python packages to speed up repeated runs:

```bash
# ensure host pip cache exists
mkdir -p ~/.cache/pip

jetson-containers run \
  -v ~/projects/doorbell_compliment_service:/workspace/doorbell_compliment_service \
  -v ~/.cache/pip:/root/.cache/pip:rw \
  -e PIP_CACHE_DIR=/root/.cache/pip \
  $(autotag l4t-pytorch)
```

This mounts your host pip cache into the container so pip downloads are reused between container runs. If the container runs as a non-root user, mount to that user's cache path or set `PIP_CACHE_DIR` accordingly. For build-time caching see the BuildKit example above.

* Switch `/doorbell` to `POST` later to handle actual camera snapshots

---

## Future Improvements

* Replace the placeholder image model with BLIP or CLIP captioning
* Integrate USB or CSI camera for live snapshots
* Add auto-reload (`uvicorn --reload`) for faster development
* Turn the container into a bootable service for always-on monitoring

---

## License

MIT License © Brad Reimer

---

## Acknowledgements

* [Jetson Containers](https://github.com/dusty-nv/jetson-containers) – Simplifying NVIDIA Jetson container workflows
* [FastAPI](https://fastapi.tiangolo.com/) – Web framework
* [TorchVision / PyTorch](https://pytorch.org/) – GPU-accelerated ML
