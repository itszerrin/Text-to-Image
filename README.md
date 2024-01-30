# DeepInfra Image Generator

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Welcome to the DeepInfra Image Generator repository! This tool allows you to generate images using the DeepInfra API with a user-friendly GUI.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Configuring `config.json`](#configuring-configjson)
- [License](#license)

## Features
- Simple and intuitive GUI for image generation.
- Command-line interface for batch processing.
- Configurable settings for customizing the image generation process.
- Automatically handles API configuration and version retrieval.

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Recentaly/Text-to-Image.git
   cd deepinfra-image-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To run the command-line version:
```bash
python tti-cli.py --prompt "Your prompt" --config /path/to/config.json --width 800 --height 600
```

To run the GUI version:
```bash
python "tti-gui.py"
```
Follow the on-screen instructions to provide input and generate images.

## Configuration
### Configuring `config.json`

The `config.json` file contains settings for your image generation. Here's an example of its structure:

```json
{
  "model": "your_model_name",
  "strength": 0.8,
  "num_interference_steps": 5,
  "guidance_scale": 0.6,
  "use_compel": true
}
```

- **model**: Specify the DeepInfra model name (e.g., "stability-ai/sdxl").
- **strength**: The strength parameter for image generation (float between 0.0 and 1.0).
- **num_interference_steps**: Number of interference steps in the generation process (integer).
- **guidance_scale**: Guidance scale for the generation process (float between 0.0 and 1.0).
- **use_compel**: Whether to use compulsion in the generation process (boolean).

Adjust these values according to your preferences and the requirements of the DeepInfra API model you're using.

## License
This project is licensed under the MIT License - see the LICENSE file for details.


