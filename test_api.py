#!/usr/bin/env python3
"""Test script for the FastAPI simplification endpoint."""

import requests
import json

SAMPLE_TEXT_01 = """Als Vernehmlassungsverfahren wird diejenige Phase innerhalb des Vorverfahrens der Gesetzgebung bezeichnet, in der Vorhaben des Bundes von erheblicher politischer, finanzieller, wirtschaftlicher, ökologischer, sozialer oder kultureller Tragweite auf ihre sachliche Richtigkeit, Vollzugstauglichkeit und Akzeptanz hin geprüft werden. 

Die Vorlage wird zu diesem Zweck den Kantonen, den in der Bundesversammlung vertretenen Parteien, den Dachverbänden der Gemeinden, Städte und der Berggebiete, den Dachverbänden der Wirtschaft sowie weiteren, im Einzelfall interessierten Kreisen unterbreitet."""

SAMPLE_TEXT_02 = """Die Zuständigkeiten des Bundesrates sind in der Bundesverfassung in den Artikeln 180 bis 187 beschrieben. An erster Stelle steht das Stichwort „Regierungspolitik“. In diesem Begriff steckt das eigentliche „Regieren. Die Bundesverfassung sagt auch, was darunter zu verstehen ist. Laut Verfassung:

    bestimmt der Bundesrat die Ziele seiner Politik und plant den Einsatz der für die Zielerreichung nötigen Ressourcen;
    informiert er die Öffentlichkeit rechtzeitig über seine Tätigkeiten.

Weitere Aufgaben des Bundesrats

Rechtsetzung und Vollzug des Rechts

Der Bundesrat unterbreitet dem Parlament Vorschläge für die Umsetzung von Volksinitiativen und für Gesetze. In eigener Kompetenz erlässt er in Verordnungen die Ausführungsbestimmungen zu Gesetzen. Er vollzieht Beschlüsse der Bundesversammlung, die nicht dem Referendum unterstehen, zum Beispiel Aufträge für Planungen.

Führung der Bundesfinanzen

Der Bundesrat führt den Bundeshaushalt. Er unterbreitet dem Parlament einen mehrjährigen Finanzplan und ein jährliches Budget. Mit der Staatsrechnung legt er dem Parlament Rechenschaft über die Verwendung der Mittel ab."""


def test_simplify_endpoint():
    """Test the POST / endpoint with sample data."""
    url = "http://127.0.0.1:8000/"

    # Sample payload
    payload = {
        "data": [
            {"text": SAMPLE_TEXT_01},
            {"text": SAMPLE_TEXT_02},
        ],
        "leichte_sprache": False,
        "model": None,  # Use default model
    }

    print(f"Testing endpoint: {url}")
    print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}\n")

    try:
        response = requests.post(url, json=payload)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}\n")

        if response.status_code == 200:
            print("✅ Success!")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print("❌ Error!")
            print(f"Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure the FastAPI server is running!")
        print("Run: uv run uvicorn fastapi_app:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_with_leichte_sprache():
    """Test with leichte_sprache enabled."""
    url = "http://127.0.0.1:8000/"

    payload = {
        "data": [{"text": SAMPLE_TEXT_01}, {"text": SAMPLE_TEXT_02}],
        "leichte_sprache": True,
        "model": None,
    }

    print("\n" + "=" * 60)
    print("Testing with leichte_sprache=True")
    print("=" * 60 + "\n")
    print(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}\n")

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✅ Success!")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        else:
            print("❌ Error!")
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("FastAPI Endpoint Test")
    print("=" * 60 + "\n")

    # Test basic endpoint
    test_simplify_endpoint()

    # Test with leichte_sprache
    test_with_leichte_sprache()

    print("\n" + "=" * 60)
    print("Tests completed!")
