# Doorbell Compliment Service

A FastAPI microservice running on my Jetson Orin Nano.  
Home Assistant sends a snapshot from my Ring doorbell, and this service analyzes the visitor’s appearance and returns a personalized compliment.

This project is designed to be lightweight, easy to deploy, and fun to extend. It integrates cleanly with Home Assistant automations and runs efficiently on NVIDIA Jetson hardware.

---

## 🚪 How It Works

1. Home Assistant detects a Ring doorbell press.
2. Home Assistant captures a snapshot and sends it to this service.
3. The Jetson analyzes the image using a lightweight vision model.
4. The service generates a contextual compliment based on visual cues.
5. Home Assistant receives the compliment and can:
   - Send it as a phone notification  
   - Speak it via TTS  
   - Store it in a dashboard  
   - Log it for history  

---

## 🧠 Features

- FastAPI endpoint: `POST /compliment`
- Lightweight image processing (EfficientNet-based)
- Simple, modular compliment generation
- Easy integration with Home Assistant
- Runs inside the Jetson L4T PyTorch container
- Fully open-source under the Apache 2.0 license

---

## 📦 Project Structure

```plain
doorbell_compliment_service/
    api/
        main.py          # FastAPI entrypoint
        vision.py        # Image feature extraction
        compliment.py    # Compliment generation logic
    requirements.txt
    README.md
    .gitignore
```

---

## ▶️ Running the Service

Inside your Jetson’s L4T PyTorch container:

```bash
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The service will be available at:

```plain
http://helmholtz.local:8000/compliment
```

---

## 🛠 Home Assistant Integration

Home Assistant should:

- Capture a Ring snapshot  
- POST it to this service  
- Use the returned compliment however you like  

See your Home Assistant automation for details.

---

## 🧪 Testing Manually

```bash
curl -X POST -F "file=@test.jpg" http://helmholtz.local:8000/compliment
```

---

## 📄 License

This project is licensed under the **Apache License 2.0**.  
You are free to use, modify, and redistribute this code, provided you include attribution.

---

## 🌱 Future Enhancements

- CLIP-based appearance analysis  
- Small LLM for richer compliments  
- TensorRT optimization  
- Logging + compliment history dashboard  
- Personality modes (warm, funny, poetic, dramatic)

---

## ✨ Author

**Brad Reimer**  
GitHub: [bradreimer](https://github.com/bradreimer)
