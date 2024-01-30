```bash

python tti-cli.py --prompt "Hyper-realistic image of a dog. Close up shot of it's face." --config "config.json" --width 512 --height 512  --output-name "EXAMPLE_1.png"
```

What my config.json looked like:

```json
{
    "model": "prompthero/openjourney",
    "guidance_scale": 11
}
```