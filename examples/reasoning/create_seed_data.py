import os
from datasets import Dataset, load_dataset
from tqdm import tqdm
from glob import glob

# output directory
output_dir = f"sdg_demo_output/"

chunk_size = 50
max_model_context_length = 2048

try:
    eng_dataset = load_dataset(
        "ai4bharat/sangraha", data_dir="verified/hin", streaming=True
    )["train"]

    eng_documents = []

    max_documents = 10
    doc_count = 0
    for each_doc in tqdm(eng_dataset, desc="For each document"):
        eng_documents.append(each_doc)
        doc_count += 1

        if doc_count >= max_documents:
            break

    seed_data = Dataset.from_list(eng_documents)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{output_dir}/seed_data.jsonl"

    seed_data.to_json(output_file, orient="records", lines=True, force_ascii=False)
except Exception as e:
    print(f"Failed to load Kannada Wikipedia dataset: {e}")
    print("Please ensure you have internet connectivity and the dataset is available.")
    exit(1)
