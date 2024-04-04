# Import necessary libraries
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import uvicorn
import aiofiles
import csv
import os

# Initialize the FastAPI app
app = FastAPI()

# Define a directory to store uploaded images and CSV files
UPLOAD_DIRECTORY = "uploaded_images"
CSV_DIRECTORY = "nutrition_info"

# Create directories if they don't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(CSV_DIRECTORY, exist_ok=True)

# Create a POST endpoint to upload an image
@app.post("/upload-image/")
async def upload_image(image: UploadFile = File(...)):
    # Save the uploaded image to a file
    file_path = f"{UPLOAD_DIRECTORY}/{image.filename}"
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await image.read()  # Read image contents
        await out_file.write(content)  # Save to file

    # Placeholder for processing the image and extracting nutritional information
    # You would need a model or an API that can analyze the image and provide the nutritional info
    nutritional_info = {
        "Item": "Example Item",
        "Calories": 100,
        "Protein": "10g",
        "Carbohydrates": "20g",
        "Fats": "5g"
    }

    # Generate CSV file from nutritional information
    csv_filename = image.filename.rsplit(".", 1)[0] + ".csv"
    csv_file_path = f"{CSV_DIRECTORY}/{csv_filename}"
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = nutritional_info.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(nutritional_info)

    # Return the CSV file as response
    return FileResponse(path=csv_file_path, filename=csv_filename, media_type='text/csv')

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
