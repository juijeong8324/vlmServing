#!/usr/bin/env python3
"""Download Qwen2-VL model weights from HuggingFace Hub."""
from pathlib import Path

import yaml
from huggingface_hub import snapshot_download


def main() -> None:
    config_path = Path(__file__).parent.parent / "configs" / "model_config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)

    model_name: str = config["model"]["name"]
    local_dir = Path(__file__).parent.parent / "model" / "weights" / model_name.replace("/", "--")
    local_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {model_name} → {local_dir}")
    snapshot_download(repo_id=model_name, local_dir=str(local_dir))
    print("Download complete!")


if __name__ == "__main__":
    main()
