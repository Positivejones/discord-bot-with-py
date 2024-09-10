import http.client
import os
import json
import requests

def download_instagram_video(url, output_folder):


    conn = http.client.HTTPSConnection("instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com")

    headers = {
    'x-rapidapi-key': "a6fe7a43dfmsh76fd373d92ba1a4p137a79jsn68de5e3bf545",
    'x-rapidapi-host': "instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com"
    }

    conn.request("GET", f"/get-info-rapidapi?url={url}", headers=headers)

    res = conn.getresponse()
    data = res.read()

# Parse the JSON response
    data_json = json.loads(data.decode("utf-8"))

# Extract the video download URL
    video_url = data_json["download_url"]

# Create the "videos" folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

# Download the video
    response = requests.get(video_url, stream=True)

# Construct the output filename with an mp4 extension
    filename = "salam.mp4"

# Save the video to the "videos" folder
    with open(os.path.join(output_folder, filename), "wb") as f:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

# Print a success message
    print(f"Video downloaded successfully to {os.path.join(output_folder, filename)}")


