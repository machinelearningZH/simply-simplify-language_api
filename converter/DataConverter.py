from model.StructuredData import SimplificationResponse


class DataConverter:

    def __init__(self, payload, simplifier, model: str = None) -> None:
        self.simplifier = simplifier

        if model:
            simplifier.set_model(model)

        self.json = payload.data
        self.leichte_sprache = bool(payload.leichte_sprache)

    def simplify(self):
        results = self.simplifier.simplify_text(self.json, self.leichte_sprache)

        # Parse the JSON string into a Python dictionary
        data = results.dict()

        # Iterate over each item in the "simplifications" list
        for item in data["simplifications"]:
            # Replace ß with ss in the "text" key
            item["text"] = item["text"].replace("ß", "ss")

        # Convert the updated dictionary back to a JSON string
        simplifications = SimplificationResponse.parse_obj(data)

        return simplifications
