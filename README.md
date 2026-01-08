# Doorbell Compliment Service

A Jetson-powered web service that analyzes doorbell images, analyzes the visitor's appearance, then returns a personalized compliment.

This project runs on **NVIDIA Jetson Orin Nano** using [jetson-containers](https://github.com/dusty-nv/jetson-containers) and `l4t-pytorch`, providing a lightweight FastAPI endpoint to handle incoming images and generate compliments (or descriptions) of visitors.

---

## Features

* FastAPI web server at `/doorbell` (default `GET` endpoint for testing)
* GPU-accelerated image analysis with PyTorch / TorchVision
* Compatible with JetPack 6 / L4T 36.x
* Fully editable via VS Code Remote SSH
* Easy containerized workflow with jetson-containers
* Clean GitHub repository layout

---

## Repository Layout

```
doorbell_compliment_service/
├── app/
│   ├── main.py            # FastAPI server entry point
│   ├── model.py           # Image analysis model
│   ├── image_utils.py     # Optional image helpers
│   └── requirements.txt   # Python dependencies
├── jetson/
│   └── dockerfile.doorbell # Jetson container Dockerfile (optional)
├── scripts/
│   └── dev.sh             # Convenience launcher
├── README.md
└── .gitignore
```

---

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

Or to speed up the installation of dependencies:

```bash
jetson-containers run \
  -v ~/projects/doorbell_compliment_service:/workspace/doorbell_compliment_service \
  -v ~/.cache/pip:/root/.cache/pip \
  $(autotag l4t-pytorch)
```

Inside the container:

```bash
cd /workspace/doorbell_compliment_service
pip install -r app/requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

The server will start on `localhost:8080`.

---

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
jetson-containers run \
  -v ~/projects/doorbell_compliment_service:/workspace/doorbell_compliment_service \
  -v ~/.cache/pip:/root/.cache/pip \
  $(autotag l4t-pytorch)
```

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
