from source.Api import Api
import argparse
import json
import logging
import requests
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")	
logger = logging.getLogger(__name__)

# Set up argument parser
parser = argparse.ArgumentParser(description="Generate images using DeepInfra API")

# Add command-line arguments
parser.add_argument("--prompt", type=str, help="Prompt to generate image from", required=True)
parser.add_argument("--config", type=str, help="Path for the config file", required=True)
parser.add_argument("--width", type=int, help="Width of the image to be generated", required=True)
parser.add_argument("--height", type=int, help="Height of the image to be generated", required=True)
parser.add_argument("--output-dir", type=str, nargs="*", help="Directory to save the generated image", default="output")
parser.add_argument("--output-name", type=str, help="Filename to save the generated image as", default="generated-output.png")

# Parse command-line arguments
args = parser.parse_args()

# Try accessing the config file
logging.info(f"Trying to access config file: {args.config}...")
try:
    with open(args.config, "r") as f:
        config = json.load(f)
        
        # in the models name, delete everything before and including the last slash
        model_name = config["model"].split("/")[-1]

        # Check for needed entries in the models config file
        with open(f"source/models/{model_name}.json", "r") as model_config:

            # Load the config file
            model_config = json.load(model_config)

            for entry in model_config["keys"]:
                if entry not in config:
                    logger.error(f"Entry {entry} not found in provided config file! Checking if default value exists...")

                    # Iterate over defaults and find the matching entry
                    default_value = None
                    for default_entry in model_config["defaults"]:
                        if entry in default_entry:
                            default_value = default_entry[entry]
                            break

                    config[entry] = default_value

                    logger.info(f"Default value {config[entry]} added for entry {entry}!")
                
        logger.info("Config file loaded! Retrieving version...")

        # Get the version
        try:

            __url = f"https://api.deepinfra.com/models/{config['model']}"

            # Make request
            response = requests.get(__url)

            response.raise_for_status()

            # Get the version
            version = response.json()["version"]

            logging.info(f"Version: {version}")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error while trying to get version: {e}")
            raise e


except FileNotFoundError:
    logger.error(f"Config file {args.config} not found!")
    raise FileNotFoundError(f"Config file {args.config} not found!")
except PermissionError:
    logger.error(f"Permission denied for config file {args.config}!")
    raise PermissionError(f"Permission denied for config file {args.config}!")

# Set up API
api = Api(config["model"], version, model_config["output_path"], model_config["has_url"])

# Generate example image
image = api.generate(
    args.prompt,
    args.width, 
    args.height, 
    config["strength"], 
    config["num_interference_steps"],
    config["guidance_scale"], 
    config["use_compel"],
)
logger.info(f"Image generated in {api.runtime} ms!")

# check if output directory exists
if not os.path.exists(args.output_dir):
    logger.info(f"Output directory {args.output_dir} does not exist! Creating...")
    os.makedirs(args.output_dir)

# Save the returned BYTESIO
with open(f"{args.output_dir}/{args.output_name}", "wb") as f:
    f.write(image)