from fastapi import FastAPI

app = FastAPI()

@app.get("/doorbell")
def doorbell():
    compliment = 'TESTING: A visitor is at the door.'
    return { "compliment": compliment }

# from fastapi import FastAPI, UploadFile, File, HTTPException
# from app.vision import extract_features
# from app.compliment import generate_compliment
# from PIL import Image
# import io

# app = FastAPI(title="Doorbell Compliment Service")


# @app.post("/compliment")
# async def compliment_endpoint(file: UploadFile = File(...)):
#     # Validate file type
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="File must be an image")

#     # Read image bytes
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents)).convert("RGB")

#     # Extract features from the image
#     features = extract_features(image)

#     # Generate a compliment based on features
#     compliment = generate_compliment(features)

#     return {"compliment": compliment}

