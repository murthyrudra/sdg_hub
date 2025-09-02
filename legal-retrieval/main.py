import os
from sdg_hub.core.flow import Flow
from datasets import Dataset
from dotenv import dotenv_values

config = dotenv_values(".env")

if "RITS_API_KEY" in config:
    api_key = config["RITS_API_KEY"]


def read_md_files(root_folder):
    md_contents = {}
    md_contents["document"] = []
    md_contents["filename"] = []
    md_contents["domain"] = []

    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".md") and "README" not in file:
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    md_contents["document"].append(f.read())
                md_contents["filename"].append(file_path)
                md_contents["domain"].append("Legal")

    return md_contents


def main():
    # Load a flow
    flow = Flow.from_yaml("query_generation.yaml")

    # Discover recommended models
    default_model = flow.get_default_model()
    print(f"Default model: {default_model}")

    # Get all recommendations
    recommendations = flow.get_model_recommendations()
    print(f"Compatible models: {recommendations['compatible']}")
    print(f"Experimental models: {recommendations['experimental']}")

    # Configure model at runtime
    flow.set_model_config(
        model="hosted_vllm/openai/gpt-oss-20b",
        api_base="https://inference-3scale-apicast-production.apps.rits.fmaas.res.ibm.com/gpt-oss-20b/v1/",
        extra_headers={"RITS_API_KEY": api_key},  # your server’s expected auth header
        extra_body={"no-log": True},
    )

    all_sections = read_md_files("data/bns_sections/")

    dataset = Dataset.from_dict(all_sections)

    # Execute the complete flow
    result = flow.generate(dataset, checkpoint_dir="output/checkpoint_dir/")
    result.to_json("output/final_dir/legal.jsonl", force_ascii=False)


if __name__ == "__main__":
    main()
