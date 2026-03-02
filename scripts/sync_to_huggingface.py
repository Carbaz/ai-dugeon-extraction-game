"""Sync the repository content to a Hugging Face Space."""

from huggingface_hub import HfApi

HfApi().upload_folder(
    folder_path=".",
    repo_id="Carbaz/the_neural_nexus",
    repo_type="space",
    delete_patterns=["*"],
    ignore_patterns=[".git/**", ".github/**", "scripts/**", ".env"],
    commit_message="Sync from GitHub",
)
