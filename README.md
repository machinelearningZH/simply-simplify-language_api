# Simple Simplifier API

**Simply Simplify German Language -- API Version**

This is a simplified version of our [Language Simplification Tool](https://github.com/machinelearningZH/simply-simplify-language).

With this version you can pip install the core functionality and use language simplification via GPT-4o as a package. The API is built with [FastAPI](https://fastapi.tiangolo.com/) and can be used to simplify German language text in production environments where you want to integrate programmatically with other services.

## Usage

- Create a [Conda](https://docs.anaconda.com/miniconda/) environment: `conda create -n simplifier python=3.9`
- Activate the environment: `conda activate simplifier`
- Clone this repository. Change into the project directory.
- Install the requirements: `pip install -r requirements.txt`
- Export the OpenAI API key as an environment variable: `export OPENAI_API_KEY=your-api-key`

**Start the FastAPI server**

- `uvicorn fastapi_app:app --reload`

**Test the API**

- Open the notebook `simple-simplifier.ipynb` and follow the instructions.

## Feedback and Contributions

Please share your feedback. You can [write an email](mailto:datashop@statistik.zh.ch) or share your ideas by opening an issue or a pull requests.

Please note, we use [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting with default settings.

# How to use the API

### Route

```POST / ```

***Description***

This endpoint simplifies a given input based on the provided payload. It supports both JSON and text formats for the input data. Depending on the specified format, the data is processed differently.

### Request Body

| Field             | Type               | Required       | Description                                                                                  |
|-------------------|--------------------|----------------|----------------------------------------------------------------------------------------------|
| `data`            | `string` or `dict` | Yes            | The input data to be simplified. Can be plain text or a JSON object.                         |
| `leichte_sprache` | `boolean`          | Yes            | If `True`, simplifies the text into plain language.                                          |
| `format`          | `string`           | Yes            | Specifies the format of the input. Accepted values are `"json"` or `"text"`.                 |
| `path`            | `string`           | Yes (for JSON) | The JSON path to target specific parts of the input data (only used if `format` is `"json"`). |
| `root`            | `string`           | Yes (for JSON) | The root key for the JSON object (only used if `format` is `"json"`).                        |
| `model`           | `gpt-4o`           | No             | Used for testing the OpenAI model, default is `gpt-4o`                                        |


```POST / ```

### JSON

```
{
    "data": {
        "id": "1",
        "fields": [
            {
                "name": "field_title",
                "type": "plaintext",
                "content": "Als Vernehmlassungsverfahren wird diejenige Phase innerhalb des Vorverfahrens der Gesetzgebung bezeichnet, in der Vorhaben des Bundes von erheblicher politischer, finanzieller, wirtschaftlicher, ökologischer, sozialer oder kultureller Tragweite auf ihre sachliche Richtigkeit, Vollzugstauglichkeit und Akzeptanz hin geprüft werden. "
            },
            {
                "name": "field_lead",
                "type": "markup",
                "content": "<p>Die Vorlage wird zu diesem <strong>Zweck</strong> den Kantonen, den in der Bundesversammlung vertretenen Parteien, den Dachverbänden der Gemeinden, Städte und der Berggebiete, den Dachverbänden der Wirtschaft sowie weiteren, im Einzelfall interessierten Kreisen unterbreitet.</p>"
            }
        ]
    },
    "leichte_sprache": "True",
    "format": "json",
    "path": "fields[*].content",
    "root": "fields"
}
```

Target specific values of the JSON with  the library  [jsonpath_ng](https://pypi.org/project/jsonpath-ng/)

***In this example***

> fields[*].content

```
{
    "id": "1",
    "fields": [
        {
            "name": "field_title",
            "type": "plaintext",
            "content": "Als Vernehmlassungsverfahren wird diejenige Phase innerhalb des Vorverfahrens der Gesetzgebung bezeichnet, in der Vorhaben des Bundes von erheblicher politischer, finanzieller, wirtschaftlicher, ökologischer, sozialer oder kultureller Tragweite auf ihre sachliche Richtigkeit, Vollzugstauglichkeit und Akzeptanz hin geprüft werden. "
        },
        {
            "name": "field_lead",
            "type": "markup",
            "content": "<p>Die Vorlage wird zu diesem <strong>Zweck</strong> den Kantonen, den in der Bundesversammlung vertretenen Parteien, den Dachverbänden der Gemeinden, Städte und der Berggebiete, den Dachverbänden der Wirtschaft sowie weiteren, im Einzelfall interessierten Kreisen unterbreitet.</p>"
        }
    ]
}
```
***Another example***

> $[*].text

```
[
    {"text": "Hello World 2"},
    {"text": "<p>Lorem ipsum dolor amet</p>"}
]
```


***Example Response (JSON Format)***

For fields[*].content

```
{
    "uuid": "1",
    "type": "section_title",
    "fields": [
        {
            "name": "field_title",
            "type": "plaintext",
            "content": "Als Vernehmlassungsverfahren wird diejenige Phase innerhalb des Vorverfahrens der Gesetzgebung bezeichnet, in der Vorhaben des Bundes von erheblicher politischer, finanzieller, wirtschaftlicher, ökologischer, sozialer oder kultureller Tragweite auf ihre sachliche Richtigkeit, Vollzugstauglichkeit und Akzeptanz hin geprüft werden. ",
            "simplified_text": "Ein Vernehmlassungsverfahren ist ein wichtiger Teil bei neuen Gesetzen. \n\nIn dieser Phase prüft der Bund neue Pläne. \n\nDer Bund prüft, ob die Pläne richtig sind. \n\nDer Bund prüft, ob die Pläne praktisch sind. \n\nDer Bund prüft, ob die Pläne akzeptiert werden. \n\nDiese Prüfung ist wichtig für:\n\n- Politik\n- Finanzen\n- Wirtschaft\n- Umwelt\n- Soziales\n- Kultur"
        },
        {
            "name": "field_lead",
            "type": "markup",
            "content": "<p>Die Vorlage wird zu diesem <strong>Zweck</strong> den Kantonen, den in der Bundesversammlung vertretenen Parteien, den Dachverbänden der Gemeinden, Städte und der Berggebiete, den Dachverbänden der Wirtschaft sowie weiteren, im Einzelfall interessierten Kreisen unterbreitet.</p>",
            "simplified_text": "<p>\nDie Vorlage geht an viele Gruppen. \nDie Vorlage geht an die Kantone. \nDie Vorlage geht an die Parteien im Parlament. \nDie Vorlage geht an die Verbände von Gemeinden und Städten. \nDie Vorlage geht an die Verbände von Berggebieten. \nDie Vorlage geht an die Wirtschafts-Verbände. \nDie Vorlage geht auch an andere interessierte Gruppen. \n</p>"
        }
    ],
    "simplification": "leichte_sprache"
}
```

```simplified_text``` will be append to the ```root``` path of the json specified. If no root specified it will be append to the JSON.

### TEXT

***Example Request (Text Format)***

```POST /```

```
{
    "data": "Lorem ipsum dolor sit amet.",
    "leichte_sprache": true,
    "format": "text"
}
```
***Example Response (Text Format)***

```
{
    "simplified_data": "Simplified plain text version."
}
```

***Responses***

    200 OK: Successfully simplified the input data. Response contains the simplified text or JSON object.
    400 Bad Request: If the required fields are missing or the payload is not correctly formatted.
    500 Internal Server Error: If an internal error occurs during processing (e.g., incorrect JSON format).

***Error Handling***

If the provided format is "json" but data is not a dictionary, the endpoint will raise a BadFormattingError.
Usage Notes

    Use "format": "json" if you're providing structured data in JSON format; otherwise, use "format": "text" for plain text.
    The leichte_sprache flag simplifies the content to plain language for easier understanding.