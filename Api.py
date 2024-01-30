# ------------------------------------------- IMPORTS ------------------------------------------- #
import requests
import json
from io import BytesIO
import base64

# for a fake user-agent
from fake_useragent import UserAgent

# for typing
from typing import Dict, Union

# ------------------------------------------- TYPING ------------------------------------------- #
Image = Union[bytes, str]

# ------------------------------------------- CONSTANTS ------------------------------------------- #

# load headers
headers: Dict[str, str] = json.load(open("source\headers\default_headers.json", "r"))

# modify headers: user-agent, content-length 
headers["User-Agent"] = UserAgent().random
headers["Content-Length"] = str(len(json.dumps(headers)))

# ------------------------------------------- MAIN API CLASS ------------------------------------------- #
class Api(object):

    def __init__(self, model, version: str, output_path: str, has_url: bool):

        self.url: str = f"https://api.deepinfra.com/v1/inference/{model}?version={version}"

        # set up session
        self.session = requests.Session()

        # set up headers
        self.session.headers.update(headers)    

        self.runtime = 0

        self.output_path = output_path  

        self.has_url = has_url

    def generate(self, prompt: str, width: int, height: int, strength: float, num_interference_steps: int, guidance_scale: float, use_compel: bool) -> Image:

        # set up payload
        payload = {
            "prompt": prompt,
            "width": width,
            "height": height,
            "strength": strength,
            "num_interference_steps": num_interference_steps,
            "guidance_scale": guidance_scale,
            "use_compel": use_compel
        }

        # special error: sdxl models require a different payload
        if "stability-ai/sdxl" in self.url:

            payload = {
                "input": {
                    "prompt": prompt,
                    "width": width,
                    "height": height,
                    "strength": strength,
                    "num_interference_steps": num_interference_steps,
                    "guidance_scale": guidance_scale,
                    "use_compel": use_compel
                }
            }

        # make requests
        response = self.session.post(self.url, json=payload)
        response.raise_for_status()

        # return raw image data in base64
        response_image_url = response.json()[self.output_path][0]

        # copy time to generate image
        self.runtime = response.json()["inference_status"]["runtime_ms"]

        if self.has_url:

            # make request
            response = requests.get(response_image_url)

            response.raise_for_status()

            # return raw image data
            return response.content
        
        else:

            base64_data = response.json()[self.output_path][0].split(",")[1]

            img_data = base64.b64decode(base64_data)

            img_data = BytesIO(img_data).read()

            return img_data


        