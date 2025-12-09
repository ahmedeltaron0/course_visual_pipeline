import requests
import json
from core.config import Settings

settings = Settings()

url = "https://platform.higgsfield.ai/nano-banana-pro"

headers = {
    "Content-Type": "application/json",
    "hf-api-key": settings.HF_API_KEY,
    "hf-secret": settings.HF_API_SECRET
}

data = {
    "num_images": 1,
    "resolution": "2k",
    "aspect_ratio": "4:3",
    "output_format": "png",
    "prompt": """{
              "style": "Ultra-realistic 8K, cinematic, with enhanced material micro-details and lifelike depth of field",
              "camera_lens": "35mm lens",
              "environment": "Well-organized industrial chemical storage room with metal shelving, labeled plastic and metal containers of cleaning and disinfecting products, safety signage on the walls, and a clean epoxy floor",
              "characters": "Arab male worker in full PPE including reflective safety vest, white hard helmet, protective nitrile gloves, and safety shoes, standing near a shelf while holding two different cleaning product bottles and looking at them thoughtfully",
              "scene": "The worker stands between tall shelves, hesitating as he compares two different chemical containers, suggesting he is about to mix them without understanding the risks, with hazard pictograms visible on the labels",
              "camera": "Horizontal 16:9 composition, eye-level perspective with a slight three-quarter angle, shallow depth of field focusing on the worker and containers, background shelves softly blurred",
              "lighting": "Soft but directional overhead industrial lighting with natural-looking reflections on plastic and metal surfaces, deep contrast and crisp shadows that emphasize labels and hazard symbols",
              "details": "Extremely detailed textures on plastic containers, realistic printed labels with small text and hazard icons, subtle wear on shelving paint, accurate reflections on glossy surfaces, realistic fabric weave on the reflective vest, visible skin texture on the worker’s face, natural creases in PPE clothing, and faint dust particles in the air",
              "extra_details": "Overall mood conveys subtle tension and educational focus on chemical safety, with consistent color palette and environment to match later scenes of chemical reactions and accidents"
            }"""
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print("Success:", result)
else:
    print("Error:", response.status_code, response.text)
