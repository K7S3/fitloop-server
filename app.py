# Import necessary libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import uvicorn
import csv
import os
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Define a directory to store CSV files
CSV_DIRECTORY = "nutrition_info"

# Create directory if it doesn't exist
os.makedirs(CSV_DIRECTORY, exist_ok=True)

# Define the request body model
class ImageRequest(BaseModel):
    image: str

# Create a POST endpoint to process an image
@app.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Process the uploaded image file
        image_data = await file.read()

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
        csv_filename = "nutritional_info.csv"
        csv_file_path = f"{CSV_DIRECTORY}/{csv_filename}"
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = nutritional_info.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(nutritional_info)

        # Return the CSV file as response
        return FileResponse(path=csv_file_path, filename=csv_filename, media_type='text/csv')
    except Exception as e:
        # Raise an HTTPException with status code 500 for any errors
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)