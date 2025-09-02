# 📄 RAG Demo for Legal Demo

This project showcases the use of [`sdg_hub`](https://pypi.org/project/sdg-hub/) for generating synthetic queries and answer based on Bharatiya Nayay Sanhita (BNS) sections. 

The project processes Markdown (`.md`) files containing indivdual BNS sections, loads them into a dataset, and runs them through a configurable **query generation flow** using [`sdg_hub`](https://pypi.org/project/sdg-hub/) to generate queries and answers.

## 📦 Installation

- Install SDG_Hub
- Configuration
  - Create a .env file in the project root with your API key:

        RITS_API_KEY=your_api_key_here

## Folder Structure
```graphql
.
├── data/
│   └── bns_sections/      # Folder with BNS Sections
├── main.py                # Entry point
├── prompts/
│   ├── prompt_answer.yaml
│   ├── prompt_explanation_satisfactory.yaml
│   ├── prompt_scenario_relevant.yaml
│   ├── prompt_scenario.yaml
│   └── prompt_translate.yaml
├── query_generation.yaml  # Flow configuration file
└── README.md
```

## Usage

- Run the pipeline:
```
python main.py
```
This will:
- Load and parse .md files from data/bns_sections/.
- Initialize a flow from query_generation.yaml.
- Run the SDG HUB flow
- Save results to: `output/final_dir/legal.jsonl`

## Pipeline

```mermaid
sequenceDiagram
    participant Input as Input Dataset
    participant Dup as DuplicateColumnsBlock<br/>(backup_document)
    participant PB1 as PromptBuilderBlock<br/>(build_scenario_prompt)
    participant LLM1 as LLMChatBlock<br/>(generate_scenario)
    participant F1 as ColumnValueFilterBlock<br/>(invalid_scenario)
    participant PB2 as PromptBuilderBlock<br/>(build_explanation_prompt)
    participant LLM2 as LLMChatBlock<br/>(generate_explanation)
    participant PB3 as PromptBuilderBlock<br/>(build_scenario_relevant_prompt)
    participant LLM3 as LLMChatBlock<br/>(generate_scenario_relevant)
    participant TP1 as TextParserBlock<br/>(extract_scenario_relevant)
    participant F2 as ColumnValueFilterBlock<br/>(drop_scenario_irrelevant)
    participant PB4 as PromptBuilderBlock<br/>(build_explanation_satisfactory_prompt)
    participant LLM4 as LLMChatBlock<br/>(generate_explanation_satisfactory)
    participant TP2 as TextParserBlock<br/>(extract_explanation_satisfactory)
    participant F3 as ColumnValueFilterBlock<br/>(drop_explanation_unsatisfactory)
    participant Output as Output Dataset

    Input ->> Dup: document → original_document
    Dup ->> PB1: document
    PB1 ->> LLM1: scenario_prompt
    LLM1 ->> F1: scenario
    F1 ->> PB2: scenario
    PB2 ->> LLM2: explanation_prompt
    LLM2 ->> PB3: explanation
    PB3 ->> LLM3: scenario_relevant_prompt
    LLM3 ->> TP1: raw_scenario_relevant
    TP1 ->> F2: scenario_relevant_score
    F2 ->> PB4: scenario
    PB4 ->> LLM4: explanation_satisfactory_prompt
    LLM4 ->> TP2: raw_explanation_satisfactory
    TP2 ->> F3: explanation_satisfactory_score
    F3 ->> Output: Valid Scenarios + Explanations
```

## 🤝 Contributing
Contributions are welcome! Please open issues or submit PRs for improvements.