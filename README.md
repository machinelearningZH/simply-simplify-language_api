# Simple Simplify Language API

**Simply Simplify German Language -- API Version**

This is a simplified version of our [Language Simplification Tool](https://github.com/machinelearningZH/simply-simplify-language).

With this version you can pip install the core functionality and use language simplification via an LLM as a package. The API is built with [FastAPI](https://fastapi.tiangolo.com/) and can be used to simplify German language text in production environments where you want to integrate programmatically with other services.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package and environment management

## Installation & Setup

### Install uv (if not already installed)

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Project

1. Clone this repository and change into the project directory
2. Create a `.env` file with your OpenAI configuration:

```bash
OPENAI_API_KEY=your_api_key_here
MODEL_NAME=gpt-4o
MAX_TOKENS=4000
```

3. Install dependencies using uv:

```bash
# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows
```

### Start the FastAPI server

```bash
uv run uvicorn fastapi_app:app --reload
```

## Development

### Adding Dependencies

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name
```

### Code Quality

We use [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting:

```bash
# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

## Feedback and Contributions

Please share your feedback. You can [write an email](mailto:datashop@statistik.zh.ch) or share your ideas by opening an issue or a pull requests.

# How to use the API

### Route

```POST /```

***Description***

This endpoint simplifies a given input based on the provided payload. It supports a JSON object for the input data.

### Request Body

| Field             | Type      | Required       | Description                                           |
|-------------------|-----------|----------------|-------------------------------------------------------|
| `data`            | `dict`    | Yes            | Json with a list of strings to simplifiy          |
| `leichte_sprache` | `boolean` | No             | If `True`, simplifies the text into plain language.   |
| `model`           | `gpt-4o`  | No             | Used for testing the OpenAI model, default is `gpt-4o` |

```POST /```

### JSON

```
{
  "data": [
        {
            "text": "Als Vernehmlassungsverfahren wird diejenige Phase innerhalb des Vorverfahrens der Gesetzgebung bezeichnet, in der Vorhaben des Bundes von erheblicher politischer, finanzieller, wirtschaftlicher, ökologischer, sozialer oder kultureller Tragweite auf ihre sachliche Richtigkeit, Vollzugstauglichkeit und Akzeptanz hin geprüft werden. "
        },
        {
            "text": "<p>Die Vorlage wird zu diesem <strong>Zweck</strong> den Kantonen, den in der Bundesversammlung vertretenen Parteien, den Dachverbänden der Gemeinden, Städte und der Berggebiete, den Dachverbänden der Wirtschaft sowie weiteren, im Einzelfall interessierten Kreisen unterbreitet.</p>"
        }
    ]
}
```

### Response

```
{
    "simplifications": [
        {
            "text": "Das Vernehmlassungsverfahren ist ein Teil der Gesetzgebung. In diesem Teil prüft der Bund wichtige Vorhaben. Der Bund prüft, ob die Vorhaben richtig, durchführbar und akzeptiert sind."
        },
        {
            "text": "Der Bund legt den Vorschlag den Kantonen vor. Auch Parteien im Parlament sehen den Vorschlag. Verbände der Gemeinden, Städte und Berggebiete bekommen den Vorschlag. Wirtschaftsverbände und andere interessierte Gruppen sehen den Vorschlag auch."
        }
    ]
}
```

***Responses***

    200 OK: Successfully simplified the input data. 
    400 Bad Request: If the required fields are missing or the payload is not correctly formatted.
    500 Internal Server Error: If an internal error occurs during processing (e.g., incorrect JSON format).

***Error Handling***

If the provided format is "json" but data is not a dictionary, the endpoint will raise a BadFormattingError.
Usage Notes
    The leichte_sprache flag simplifies the content to plain language for easier understanding.
