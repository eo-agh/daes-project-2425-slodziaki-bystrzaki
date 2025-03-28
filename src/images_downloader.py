import os
import json
import numpy as np
from sentinelhub import (
    SentinelHubRequest, 
    DataCollection, 
    MimeType, 
    CRS, 
    BBox, 
    bbox_to_dimensions, 
    SHConfig
)

def init() -> SHConfig:
    with open("config.json") as f:
        config_json = json.load(f)
        config = SHConfig()
    config.sh_client_id = config_json['SH_CLIENT_ID']
    config.sh_client_secret = config_json['SH_CLIENT_SECRET']
    config.save()
    
    return config
    

def normalize_image(image, target_mean, target_std):
    """
    Normalize an image using percentile-based contrast stretching.
    
    Parameters:
        image (numpy.ndarray): Input image as a NumPy array.
        lower_percentile (int): Lower percentile for normalization (default=2).
        upper_percentile (int): Upper percentile for normalization (default=98).

    Returns:
        numpy.ndarray: Normalized image in the range 0-255.
    """
    
    image = image.astype(np.float32)
    mean = image.mean()
    std = image.std()
    
    image = (image - mean) / std
    image = target_std * image + target_mean
    image = np.clip(image, 0, 1)

    return image


def download_image(
    lon: float, 
    lat: float, 
    bbox_size: float, 
    resolution: int, 
    config: SHConfig
):
    bbox = BBox([lon - 2 * bbox_size, lat - bbox_size, lon + 2 * bbox_size, lat + bbox_size], CRS.WGS84)
    size = bbox_to_dimensions(bbox, resolution=resolution)
    
    time_interval = ("2023-03-01", "2024-03-22")

    evalscript = """
    // SentinelHub Evalscript for cloud-free Sentinel-2 images
    function setup() {
        return {
            input: ["B04", "B03", "B02", "SCL"],
            output: { bands: 3 }
        };
    }

    function evaluatePixel(sample) {
        // Mask clouds using SCL (Scene Classification Layer)
        if (sample.SCL == 3 || sample.SCL == 8 || sample.SCL == 9 || sample.SCL == 10) {
            return [0.05, 0.05, 0.05]; // Remove clouds, cloud shadows, and snow
        }
        return [sample.B04, sample.B03, sample.B02];
    }
    """

    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=time_interval,
                mosaicking_order="leastCC"
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config
    )

    response = request.get_data()
    image = np.array(response[0])
    return normalize_image(image, 0.5, 0.2)


import os
import csv
import argparse
import numpy as np
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Download Sentinel-2 images for coordinates from a file.")
    parser.add_argument("input_file", type=str, help="Path to the CSV file containing coordinates.")
    parser.add_argument("output_dir", type=str, help="Directory to save the downloaded images.")
    parser.add_argument("--bbox_size", type=float, default=0.1, help="Bounding box size for image download.")
    parser.add_argument("--resolution", type=int, default=30, help="Resolution for SentinelHub request.")

    args = parser.parse_args()

    config = init()

    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.input_file, "r") as f:
        reader = csv.DictReader(f)  # Use DictReader to handle column names
        for row in reader:
            try:
                name = row["name"].replace(" ", "_")  # Replace spaces with underscores
                lon, lat = float(row["lon"]), float(row["lat"])
                print(f"Processing: {name} (lon={lon}, lat={lat})")

                # Download image
                image = download_image(lon, lat, args.bbox_size, args.resolution, config)

                # Convert to 8-bit image format (0-255)
                image_uint8 = (image * 255).astype(np.uint8)
                img_pil = Image.fromarray(image_uint8)

                # Save image with city name
                output_path = os.path.join(args.output_dir, f"{name}.png")
                img_pil.save(output_path)
                print(f"Saved image: {output_path}")

            except Exception as e:
                print(f"Error processing {name} ({lon}, {lat}): {e}")

if __name__ == "__main__":
    main()
