import json
from pathlib import Path

from app.data.mock_data import get_mock_shipments


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "shipments.json"


def load_shipments() -> list[dict]:
    if not DATA_FILE.exists():
        shipments = get_mock_shipments()
        save_shipments(shipments)
        return shipments

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_shipments(shipments: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(shipments, file, ensure_ascii=False, indent=2)
