#!/usr/bin/env python3
"""Reconstruct and validate the committed session-level Tableau source."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import os
import tempfile
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PART_PATTERN = "ecommerce_funnel_clean.csv.gz.part-*"
EXPECTED_COMPRESSED_SHA256 = (
    "3d6464f5c966fc1cc3971cfa81223681fa7ce53dbc65d4172f346e911d2c57bb"
)
EXPECTED_UNCOMPRESSED_SHA256 = (
    "af9b9f975924f0b7a09588c9d21b6f316a8440d88ec1e2883a0d2f3bf0d87eb9"
)
EXPECTED_HEADERS = [
    "user_id",
    "session_id",
    "date",
    "month",
    "channel",
    "campaign_type",
    "device",
    "user_type",
    "region",
    "visited_website",
    "viewed_product",
    "added_to_cart",
    "checkout_started",
    "purchase_completed",
    "discount_applied",
    "order_value",
    "revenue",
    "visited_website_flag",
    "viewed_product_flag",
    "added_to_cart_flag",
    "checkout_started_flag",
    "purchase_completed_flag",
    "discount_applied_flag",
]
FLAG_FIELDS = [
    "visited_website_flag",
    "viewed_product_flag",
    "added_to_cart_flag",
    "checkout_started_flag",
    "purchase_completed_flag",
    "discount_applied_flag",
]
EXPECTED_TOTALS = {
    "sessions": 120_000,
    "viewed_product_flag": 77_870,
    "added_to_cart_flag": 27_156,
    "checkout_started_flag": 16_234,
    "purchase_completed_flag": 8_181,
}
EXPECTED_REVENUE = Decimal("17016599.15")
EXPECTED_AOV = Decimal("2080.01")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def reconstruct(parts: list[Path]) -> bytes:
    if not parts:
        raise FileNotFoundError(
            f"No multipart dataset found at data/{PART_PATTERN}"
        )
    compressed = b"".join(part.read_bytes() for part in parts)
    actual_compressed = sha256(compressed)
    if actual_compressed != EXPECTED_COMPRESSED_SHA256:
        raise ValueError(
            "Compressed SHA-256 mismatch: "
            f"expected {EXPECTED_COMPRESSED_SHA256}, got {actual_compressed}"
        )

    try:
        payload = gzip.decompress(compressed)
    except gzip.BadGzipFile as error:
        raise ValueError("The reconstructed multipart file is not valid gzip.") from error

    actual_uncompressed = sha256(payload)
    if actual_uncompressed != EXPECTED_UNCOMPRESSED_SHA256:
        raise ValueError(
            "Uncompressed SHA-256 mismatch: "
            f"expected {EXPECTED_UNCOMPRESSED_SHA256}, got {actual_uncompressed}"
        )
    return payload


def validate(payload: bytes) -> dict[str, Decimal | int]:
    stream = io.StringIO(payload.decode("utf-8"), newline="")
    reader = csv.DictReader(stream)
    if reader.fieldnames != EXPECTED_HEADERS:
        raise ValueError(
            "Unexpected CSV columns. "
            f"Expected {EXPECTED_HEADERS}, got {reader.fieldnames}"
        )

    sessions: set[str] = set()
    stage_totals = {field: 0 for field in FLAG_FIELDS}
    revenue = Decimal("0")
    rows = 0

    for line_number, row in enumerate(reader, start=2):
        rows += 1
        session_id = row["session_id"]
        if not session_id:
            raise ValueError(f"Missing session_id on line {line_number}.")
        if session_id in sessions:
            raise ValueError(f"Duplicate session_id {session_id!r}.")
        sessions.add(session_id)

        flags: dict[str, int] = {}
        for field in FLAG_FIELDS:
            try:
                value = int(row[field])
            except ValueError as error:
                raise ValueError(
                    f"{field} is not an integer on line {line_number}."
                ) from error
            if value not in (0, 1):
                raise ValueError(
                    f"{field} must be 0 or 1 on line {line_number}."
                )
            flags[field] = value
            stage_totals[field] += value

        progression = (
            flags["visited_website_flag"],
            flags["viewed_product_flag"],
            flags["added_to_cart_flag"],
            flags["checkout_started_flag"],
            flags["purchase_completed_flag"],
        )
        if any(left < right for left, right in zip(progression, progression[1:])):
            raise ValueError(
                f"Funnel stages are not monotonic for session {session_id!r}."
            )

        try:
            revenue += Decimal(row["revenue"])
        except Exception as error:
            raise ValueError(
                f"Invalid revenue on line {line_number}: {row['revenue']!r}"
            ) from error

    if rows != EXPECTED_TOTALS["sessions"] or len(sessions) != rows:
        raise ValueError(
            f"Expected 120,000 unique sessions, found {rows:,} rows "
            f"and {len(sessions):,} unique IDs."
        )
    for field in (
        "viewed_product_flag",
        "added_to_cart_flag",
        "checkout_started_flag",
        "purchase_completed_flag",
    ):
        if stage_totals[field] != EXPECTED_TOTALS[field]:
            raise ValueError(
                f"{field} mismatch: expected {EXPECTED_TOTALS[field]:,}, "
                f"got {stage_totals[field]:,}"
            )
    if revenue != EXPECTED_REVENUE:
        raise ValueError(
            f"Revenue mismatch: expected {EXPECTED_REVENUE}, got {revenue}"
        )

    purchases = stage_totals["purchase_completed_flag"]
    average_order_value = (revenue / purchases).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    if average_order_value != EXPECTED_AOV:
        raise ValueError(
            f"Average order value mismatch: expected {EXPECTED_AOV}, "
            f"got {average_order_value}"
        )

    return {
        "sessions": rows,
        "product_views": stage_totals["viewed_product_flag"],
        "carts": stage_totals["added_to_cart_flag"],
        "checkouts": stage_totals["checkout_started_flag"],
        "purchases": purchases,
        "revenue": revenue,
        "average_order_value": average_order_value,
    }


def write_atomically(payload: bytes, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb", prefix=f".{destination.name}.", dir=destination.parent, delete=False
    ) as temporary:
        temporary.write(payload)
        temporary_path = Path(temporary.name)
    try:
        os.replace(temporary_path, destination)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct, checksum and validate the committed Tableau source."
        )
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "data" / "ecommerce_funnel_clean.csv"),
        help="Validated CSV destination (default: data/ecommerce_funnel_clean.csv)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate the multipart dataset without writing the CSV.",
    )
    args = parser.parse_args()

    parts = sorted((ROOT / "data").glob(PART_PATTERN))
    payload = reconstruct(parts)
    totals = validate(payload)

    if not args.check_only:
        destination = Path(args.output).resolve()
        write_atomically(payload, destination)
        print(f"Wrote validated Tableau source to {destination}")

    for name, value in totals.items():
        print(f"{name}: {value:,}")


if __name__ == "__main__":
    main()
