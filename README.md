# Interesting Project

This repository now includes a small Python module, `dynamic_answers.py`, that
builds narrative-rich interview responses based on curated stories from several
roles (Southwest Airlines, LinkedIn, Shearman & Sterling, and the NYC Department
of Education).

## Usage

Run the module directly to print every available story:

```bash
python dynamic_answers.py
```

To integrate it elsewhere, import the `DynamicAnswerGenerator` and call
`generate_answer` with a question type such as `"influence"`, `"failure"`, or
`"tradeoff"`.

```python
from dynamic_answers import DynamicAnswerGenerator

generator = DynamicAnswerGenerator()
print(generator.generate_answer("influence"))
```

## Extending the catalog

Add new stories by creating a `Story` instance and registering it via
`register_story`.  Stories are grouped by question type, allowing the generator
to support follow-up variants in the future.
