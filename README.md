# Simple Simplify Language API

**Simply Simplify German Language -- API Version**

![GitHub License](https://img.shields.io/github/license/machinelearningZH/simply-simplify-language_api)
[![PyPI - Python](https://img.shields.io/badge/python-v3.12+-blue.svg)](https://github.com/machinelearningZH/simply-simplify-language_api)
[![GitHub Stars](https://img.shields.io/github/stars/machinelearningZH/simply-simplify-language_api.svg)](https://github.com/machinelearningZH/simply-simplify-language_api/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/machinelearningZH/simply-simplify-language_api.svg)](https://github.com/machinelearningZH/simply-simplify-language_api/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/machinelearningZH/simply-simplify-language_api.svg)](https://github.com/machinelearningZH/simply-simplify-language_api/pulls)
[![Current Version](https://img.shields.io/badge/version-0.3-green.svg)](https://github.com/machinelearningZH/simply-simplify-language_api)
<a href="https://github.com/astral-sh/ruff"><img alt="linting - Ruff" class="off-glb" loading="lazy" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json"></a>

## Features

This is a simplified version of our [Language Simplification Tool](https://github.com/machinelearningZH/simply-simplify-language).

This API is built with [FastAPI](https://fastapi.tiangolo.com/) and provides language simplification via an LLM through HTTP endpoints. It can be used in production environments to integrate text simplification programmatically with other services.

## Installation

Requirements:

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for package and environment management

```bash
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup Project

1. Clone this repository and change into the project directory
2. Create a `.env` file with your OpenRouter configuration:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
MODEL_NAME=google/gemini-3-flash-preview
MAX_TOKENS=8096
SITE_URL=https://your-site.com  # Optional
SITE_NAME=Your App Name  # Optional
```

3. Install dependencies using uv:

```bash
# Create virtual environment and install dependencies
uv sync
```

Note: `uv run` automatically activates the virtual environment, so manual activation is not required.

### Start the FastAPI server

```bash
uv run uvicorn fastapi_app:app --reload
```

### Testing the API

A test script is provided to quickly test the API endpoint:

```bash
# In a separate terminal (while the server is running)
uv run python test_api.py
```

The test script will:

- Send sample German text to the simplification endpoint
- Test both with and without `leichte_sprache` mode
- Display the request payload and response
- Show connection errors if the server isn't running

## API Reference

### Endpoint

**`POST /`**

Simplifies German text based on the provided payload.

#### Request Body

| Field             | Type            | Required | Description                                                                                                                             |
| ----------------- | --------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `data`            | `array[object]` | Yes      | Array of text objects to simplify. Each object must have a `text` field.                                                                |
| `leichte_sprache` | `boolean`       | No       | If `true`, simplifies the text into [Leichte Sprache](https://en.wikipedia.org/wiki/Leichte_Sprache) (plain language). Default: `false` |
| `model`           | `string`        | No       | LLM model to use via OpenRouter. Default: `openai/gpt-4o`. See [OpenRouter models](https://openrouter.ai/models)                        |

#### Example Request

```json
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

### Example Response

```json
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

### Response Codes

- **200 OK**: Successfully simplified the input data
- **400 Bad Request**: Required fields are missing or the payload is incorrectly formatted
- **500 Internal Server Error**: An internal error occurred during processing

### Notes

- The `data` field must be an array of objects, where each object contains a `text` field
- HTML tags in the input text are preserved in the output
- The `leichte_sprache` option uses specific prompts to generate text that follows [Leichte Sprache](https://en.wikipedia.org/wiki/Leichte_Sprache) guidelines for easier comprehension

## Project Team

**Chantal Amrhein**, **Patrick Arnecke** – [Statistisches Amt Zürich: Team Data](https://www.zh.ch/de/direktion-der-justiz-und-des-innern/statistisches-amt/data.html)

## Feedback and Contributing

We welcome feedback and contributions! [Email us](mailto:datashop@statistik.zh.ch) or open an issue or pull request.

We use [`ruff`](https://docs.astral.sh/ruff/) for linting and formatting.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This software (the Software) incorporates the open-source model XXXXX (the Model) and has been developed according to and with the intent to be used under Swiss law. Please be aware that the EU Artificial Intelligence Act (EU AI Act) may, under certain circumstances, be applicable to your use of the Software. You are solely responsible for ensuring that your use of the Software as well as of the underlying Model complies with all applicable local, national and international laws and regulations. By using this Software, you acknowledge and agree (a) that it is your responsibility to assess which laws and regulations, in particular regarding the use of AI technologies, are applicable to your intended use and to comply therewith, and (b) that you will hold us harmless from any action, claims, liability or loss in respect of your use of the Software.
