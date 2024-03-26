import tkinter as tk
from tkinter import filedialog
from source.Api import Api
import json
import logging
import requests
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class GUIApp:
    def __init__(self, master):
        self.master = master
        master.title("DeepInfra Image Generator")

        # Create and set up the GUI elements
        self.prompt_label = tk.Label(master, text="Prompt:")
        self.prompt_entry = tk.Entry(master)

        self.config_label = tk.Label(master, text="Config File:")
        self.config_entry = tk.Entry(master)
        self.config_button = tk.Button(master, text="Browse", command=self.browse_config)

        self.width_label = tk.Label(master, text="Width:")
        self.width_entry = tk.Entry(master)

        self.height_label = tk.Label(master, text="Height:")
        self.height_entry = tk.Entry(master)

        self.output_dir_label = tk.Label(master, text="Output Directory:")
        self.output_dir_entry = tk.Entry(master)
        self.output_dir_button = tk.Button(master, text="Browse", command=self.browse_output_dir)

        self.output_name_label = tk.Label(master, text="Output Name:")
        self.output_name_entry = tk.Entry(master)

        self.generate_button = tk.Button(master, text="Generate Image", command=self.generate_image)

        # Layout the GUI elements
        self.prompt_label.grid(row=0, column=0, sticky="e")
        self.prompt_entry.grid(row=0, column=1)

        self.config_label.grid(row=1, column=0, sticky="e")
        self.config_entry.grid(row=1, column=1)
        self.config_button.grid(row=1, column=2)

        self.width_label.grid(row=2, column=0, sticky="e")
        self.width_entry.grid(row=2, column=1)

        self.height_label.grid(row=3, column=0, sticky="e")
        self.height_entry.grid(row=3, column=1)

        self.output_dir_label.grid(row=4, column=0, sticky="e")
        self.output_dir_entry.grid(row=4, column=1)
        self.output_dir_button.grid(row=4, column=2)

        self.output_name_label.grid(row=5, column=0, sticky="e")
        self.output_name_entry.grid(row=5, column=1)

        self.generate_button.grid(row=6, column=1)

    def browse_config(self):
        config_file = filedialog.askopenfilename(title="Select Config File", filetypes=[("JSON Files", "*.json")])
        self.config_entry.delete(0, tk.END)
        self.config_entry.insert(0, config_file)

    def browse_output_dir(self):
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        self.output_dir_entry.delete(0, tk.END)
        self.output_dir_entry.insert(0, output_dir)

    def generate_image(self):
        # Gather inputs from GUI elements
        prompt = self.prompt_entry.get()
        config_file = self.config_entry.get()
        width = int(self.width_entry.get())
        height = int(self.height_entry.get())
        output_dir = self.output_dir_entry.get()  if self.output_name_entry.get() else "output"
        output_name = self.output_name_entry.get() if self.output_name_entry.get() else "generated-output.png"

        # Try accessing the config file
        logging.info(f"Trying to access config file: {config_file}...")
        try:
            with open(config_file, "r") as f:
                config = json.load(f)
                model_name = config["model"].split("/")[-1]

                # Check for needed entries in the models config file
                with open(f"source/models/{model_name}.json", "r") as model_config:
                    # Load the config file
                    model_config = json.load(model_config)

                    # Check for needed entries
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
                    response = requests.get(__url)
                    response.raise_for_status()
                    version = response.json()["version"]
                    logging.info(f"Version: {version}")

                except requests.exceptions.HTTPError as e:
                    logger.error(f"Error while trying to get version: {e}")
                    raise e

        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found!")
            raise FileNotFoundError(f"Config file {config_file} not found!")
        except PermissionError:
            logger.error(f"Permission denied for config file {config_file}!")
            raise PermissionError(f"Permission denied for config file {config_file}!")

        # Set up API
        api = Api(config["model"], version, model_config["output_path"], model_config["has_url"])

        # Generate example image
        image = api.generate(
            prompt,
            width,
            height,
            config["strength"],
            config["num_interference_steps"],
            config["guidance_scale"],
            config["use_compel"],
        )
        logger.info(f"Image generated in {api.runtime} ms!")

        # check if output directory exists
        if not os.path.exists(output_dir):
            logger.info(f"Output directory {output_dir} does not exist! Creating...")
            os.makedirs(output_dir)

        # Save the returned BYTESIO
        with open(f"{output_dir}/{output_name}", "wb") as f:
            f.write(image)

# Create the main application window
root = tk.Tk()

# Initialize the GUIApp class
app = GUIApp(root)

# Run the GUI application
root.mainloop()
