import json


def consume(raw_message: str) -> None:
    message = json.loads(raw_message)
    application_id = message["application_id"]
    print(f"consume approval result for {application_id}")
