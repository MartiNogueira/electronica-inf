import json
import boto3

rekognition = boto3.client('rekognition', region_name='us-east-1')

bucket = 'esp32-captures'        # Nombre del bucket
image_name = 'patente.jpeg'      # Nombre de la imagen

response = rekognition.detect_text(
    Image={'S3Object': {'Bucket': bucket, 'Name': image_name}}
)

print(json.dumps(response, indent=4))

for item in response['TextDetections']:
    if item['Type'] == 'WORD':
        print(item['DetectedText'])

