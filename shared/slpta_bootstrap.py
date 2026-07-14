"""
slpta_bootstrap.py
==================
Shared helpers for the IPAM USL "Introduction to Artificial Intelligence"
5-week short course (Introductory tier).

Every notebook imports from this module so that:
  * the Gemini model id lives in ONE place (MODEL),
  * the synthetic SLPTA dataset is generated identically for every student,
  * the running Route R12 scenario reads the same everywhere.

Design goals
------------
* Zero-install on Google Colab: only pandas + numpy are needed to BUILD the
  data (both ship with Colab). `google-genai` is imported lazily inside
  get_client(), so Module 1 notebooks (pure scikit-learn) never need it.
* Deterministic: a fixed seed means every student gets the same numbers, so a
  facilitator can say "your accuracy should be about 0.86" and be right.
* Synthetic only: no real passengers, operators, or PII. Every value is made up.

Public API (imported by the canonical bootstrap cell)
-----------------------------------------------------
    MODEL                  -> str, the Gemini model id
    ensure_course_data()   -> Path to course_data/, generating it if missing
    get_client()           -> google-genai Client (raises a friendly error if no key)
    load_route12_context() -> str, the canonical Route R12 incident briefing

Convenience loaders (handy in labs)
-----------------------------------
    load_table("route_logs") / load_route_logs() / load_complaints() / ...
"""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Gemini model used from Day 9 onward. Free-tier friendly. If Google renames or
# retires this id, a facilitator only changes it HERE and every notebook follows.
MODEL = "gemini-3.5-flash"

# Bump this if I change the data generators and want students to regenerate.
DATA_VERSION = "1.0"

# The running scenario. Every tier and every day reuses these exact facts.
ROUTE12 = {
    "route_id": "R12",
    "name": "Wilberforce \u2192 CBD",
    "operator_id": "OP-104",
    "vehicle_id": "BUS-123",
    "delay_minutes": 25,
    "scheduled_departure": "07:45",
    "cause": "Heavy traffic on Wilkinson Road",
    "affected_passengers": 40,
}


# ---------------------------------------------------------------------------
# Locating the repo / data directory
# ---------------------------------------------------------------------------

def _repo_root() -> Path:
    """Find the folder that contains shared/slpta_bootstrap.py."""
    here = Path(__file__).resolve()
    # __file__ is .../shared/slpta_bootstrap.py -> parent is shared/, parent.parent is root
    return here.parent.parent


def data_dir() -> Path:
    """Return (and create) the course_data/ directory at the repo root."""
    d = _repo_root() / "course_data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def load_route12_context() -> str:
    """One canonical paragraph describing the Route R12 incident."""
    r = ROUTE12
    return (
        f"Route {r['route_id']} ({r['name']}). The {r['scheduled_departure']} service, "
        f"operated by {r['operator_id']} on vehicle {r['vehicle_id']}, departed "
        f"{r['delay_minutes']} minutes late. Recorded cause: {r['cause']}. "
        f"About {r['affected_passengers']} passengers were affected and the dispatch "
        f"desk received multiple complaints. (Synthetic SLPTA scenario \u2014 no real data.)"
    )


# ---------------------------------------------------------------------------
# Gemini client (lazy import so Module 1 never needs google-genai)
# ---------------------------------------------------------------------------

def get_client():
    """
    Return a google-genai Client.

    Looks for the API key in:
      1. the GEMINI_API_KEY environment variable, then
      2. Colab Secrets (the key icon in the left sidebar).

    Raises a clear, beginner-friendly error if no key is found.
    """
    try:
        from google import genai  # lazy: only Day 9+ needs this installed
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "google-genai is not installed. Run:  !pip install -q google-genai"
        ) from exc

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            from google.colab import userdata  # type: ignore

            api_key = userdata.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        raise RuntimeError(
            "No GEMINI_API_KEY found.\n"
            "In Colab: click the key icon (Secrets) in the left sidebar, add a "
            "secret named GEMINI_API_KEY, paste your key, and toggle notebook "
            "access ON. Then re-run this cell."
        )

    return genai.Client(api_key=api_key)


# ---------------------------------------------------------------------------
# Synthetic data generators
# ---------------------------------------------------------------------------

_ROUTES = [
    # route_id, name, corridor, distance_km, num_stops, scheduled_minutes, base_fare_le, popularity
    ("R12", "Wilberforce \u2192 CBD", "Western", 11.2, 18, 45, 5000, 1.00),
    ("R7",  "Lumley \u2192 CBD",       "Western", 9.4,  15, 40, 4500, 0.85),
    ("R3",  "Waterloo \u2192 CBD",     "Eastern", 28.0, 24, 80, 8000, 0.70),
    ("R21", "Goderich \u2192 Lumley",  "Peninsula", 7.1, 11, 30, 4000, 0.55),
    ("R9",  "Kissy \u2192 CBD",        "Eastern", 12.8, 19, 50, 5500, 0.80),
    ("R14", "Hill Station \u2192 CBD", "Central", 8.7, 13, 38, 4500, 0.60),
]

_WEATHER = ["Sunny", "Rain", "Heavy Rain", "Harmattan"]
_WEATHER_DELAY = {"Sunny": 0.0, "Rain": 6.0, "Heavy Rain": 14.0, "Harmattan": 3.0}
_WEATHER_P = [0.55, 0.22, 0.10, 0.13]

# NOTE: the "on time / no special cause" label is "Normal", NOT "None".
# pandas reads the literal string "None" as a missing value (NaN), which would
# wrongly show up as dirty data in the Day 2 cleaning lab.
_CAUSE_DELAY = {"Normal": 0.0, "Traffic": 12.0, "Mechanical": 20.0,
                "Weather": 0.0, "Staffing": 10.0}

_DOW = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _gen_routes() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "route_id": r[0], "name": r[1], "corridor": r[2],
                "distance_km": r[3], "num_stops": r[4],
                "scheduled_minutes": r[5], "base_fare_le": r[6],
            }
            for r in _ROUTES
        ]
    )


def _gen_operators(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for i in range(101, 121):  # OP-101 .. OP-120
        rows.append(
            {
                "operator_id": f"OP-{i}",
                "name": f"Operator {i}",
                "vehicle_count": int(rng.integers(2, 9)),
                "region": rng.choice(["Western", "Eastern", "Central", "Peninsula"]),
                "avg_rating": round(float(rng.uniform(2.8, 4.6)), 1),
                # small hidden per-operator punctuality bias used by the log generator
                "_bias": round(float(rng.normal(0, 4)), 2),
            }
        )
    return pd.DataFrame(rows)


def _gen_route_logs(rng: np.random.Generator, operators: pd.DataFrame,
                    n_days: int = 60) -> pd.DataFrame:
    """Trip-level operating log. This is the Module 1 workhorse dataset."""
    op_bias = dict(zip(operators["operator_id"], operators["_bias"]))
    op_ids = operators["operator_id"].tolist()
    routes = _gen_routes()

    start = pd.Timestamp("2025-02-03")  # a Monday
    rows = []
    trip = 1
    for day in range(n_days):
        date = start + pd.Timedelta(days=day)
        dow = _DOW[date.dayofweek]
        weekend = date.dayofweek >= 5
        for r in routes.itertuples(index=False):
            # fewer services on weekends, scaled by route popularity
            pop = dict(zip([x[0] for x in _ROUTES], [x[7] for x in _ROUTES]))[r.route_id]
            n_services = max(1, int(round((4 if weekend else 8) * pop)))
            for _ in range(n_services):
                hour = int(rng.choice(range(6, 21)))
                peak = hour in (7, 8, 17, 18) and not weekend
                weather = rng.choice(_WEATHER, p=_WEATHER_P)
                # cause_category: usually "Normal"; a "Weather" cause is only
                # plausible when it is actually raining, so we gate it on weather.
                if weather in ("Rain", "Heavy Rain") and rng.random() < (
                    0.5 if weather == "Heavy Rain" else 0.3
                ):
                    cause = "Weather"
                else:
                    cause = rng.choice(
                        ["Normal", "Traffic", "Mechanical", "Staffing"],
                        p=[0.70, 0.16, 0.06, 0.08],
                    )
                op = rng.choice(op_ids)

                base = 2.0
                effect = (
                    _WEATHER_DELAY[weather]
                    + _CAUSE_DELAY[cause]
                    + (8.0 if peak else 0.0)
                    + op_bias[op]
                    + float(rng.normal(0, 5))
                )
                delay = max(0.0, base + effect)

                passengers = int(
                    max(0, rng.normal(40 if peak else 22, 9) * pop)
                )
                rows.append(
                    {
                        "trip_id": f"T{trip:05d}",
                        "date": date.strftime("%Y-%m-%d"),
                        "day_of_week": dow,
                        "route_id": r.route_id,
                        "operator_id": op,
                        "scheduled_hour": hour,
                        "peak_period": peak,
                        "weather": weather,
                        "cause_category": cause,
                        "distance_km": r.distance_km,
                        "passenger_count": passengers,
                        "fare_leones": r.base_fare_le,
                        "delay_minutes": round(delay, 1),
                    }
                )
                trip += 1

    df = pd.DataFrame(rows)

    # Inject realistic dirtiness for the Day 2 cleaning lab -----------------
    # ~8% missing weather, ~5% missing passenger_count
    miss_w = rng.random(len(df)) < 0.08
    df.loc[miss_w, "weather"] = np.nan
    miss_p = rng.random(len(df)) < 0.05
    df.loc[miss_p, "passenger_count"] = np.nan
    # a few duplicate rows + a couple of out-of-range delays (data entry slips)
    dups = df.sample(8, random_state=1)
    df = pd.concat([df, dups], ignore_index=True)
    bad = rng.choice(df.index, 3, replace=False)
    df.loc[bad, "delay_minutes"] = df.loc[bad, "delay_minutes"] + 600  # obvious outliers

    return df


# --- complaints / tickets --------------------------------------------------

_COMPLAINT_TEMPLATES = {
    "Delay": [
        "Bus on {route} was {mins} minutes late this morning, no announcement.",
        "Waited almost an hour for {route}, completely unacceptable.",
        "{route} never showed at the scheduled time again.",
    ],
    "Overcharging": [
        "Conductor on {route} charged me {amt} above the posted fare.",
        "Operator {op} is collecting extra money and refusing change.",
        "Why did I pay {amt} when the board says the fare is lower?",
    ],
    "Safety": [
        "Driver on {route} was speeding and overtaking dangerously.",
        "The {route} vehicle had bald tyres and a broken door.",
        "Operator {op} let too many standing passengers, felt unsafe.",
    ],
    "Cleanliness": [
        "The {route} bus was filthy, seats torn and smelling.",
        "Rubbish all over the floor of the {route} vehicle.",
    ],
    "Staff Conduct": [
        "Conductor on {route} was rude and shouting at an elderly woman.",
        "Operator {op} staff refused to help with my luggage.",
    ],
    "Lost Item": [
        "I left my phone on the {route} bus this afternoon, please help.",
        "Lost a bag of documents on {route}, who do I contact?",
    ],
    "Other": [
        "Where can I get the timetable for {route}?",
        "Is {route} running during the public holiday?",
    ],
}

# Which categories tend to be urgent (used for the Day 1 labelling exercise).
_URGENT_CATS = {"Safety", "Lost Item"}
_CHANNELS = ["SMS", "Call", "WhatsApp", "InPerson"]


def _gen_complaints(rng: np.random.Generator, n: int = 400) -> pd.DataFrame:
    routes = [r[0] for r in _ROUTES]
    cats = list(_COMPLAINT_TEMPLATES)
    cat_p = [0.34, 0.14, 0.14, 0.10, 0.12, 0.08, 0.08]
    rows = []
    start = pd.Timestamp("2025-02-03 06:00")
    for i in range(1, n + 1):
        cat = rng.choice(cats, p=cat_p)
        tmpl = rng.choice(_COMPLAINT_TEMPLATES[cat])
        route = rng.choice(routes, p=[0.30, 0.16, 0.10, 0.10, 0.18, 0.16])
        op = f"OP-{int(rng.integers(101, 121))}"
        text = tmpl.format(
            route=route, op=op,
            mins=int(rng.integers(10, 55)),
            amt=f"{int(rng.integers(500, 3000))} Le",
        )
        # severity: urgent categories skew High
        if cat in _URGENT_CATS:
            sev = rng.choice(["Low", "Medium", "High"], p=[0.1, 0.3, 0.6])
        else:
            sev = rng.choice(["Low", "Medium", "High"], p=[0.45, 0.4, 0.15])
        ts = start + pd.Timedelta(minutes=int(rng.integers(0, 60 * 24 * 60)))
        rows.append(
            {
                "ticket_id": f"C{i:04d}",
                "timestamp": ts.strftime("%Y-%m-%d %H:%M"),
                "channel": rng.choice(_CHANNELS, p=[0.4, 0.3, 0.2, 0.1]),
                "route_id": route,
                "raw_text": text,
                "category": cat,            # gold label
                "severity": sev,
                "is_urgent": (sev == "High") or (cat in _URGENT_CATS),
                "resolved": bool(rng.random() < 0.55),
            }
        )
    return pd.DataFrame(rows)


# --- short policy documents (for Day 9-10 LLM labs) -----------------------

_POLICIES = {
    "delay_communication_policy.md": """# SLPTA Delay Communication Policy (Synthetic)

1. Any service delayed more than 15 minutes must be logged in the dispatch
   system with a cause category.
2. For delays over 20 minutes on a peak service, dispatch must issue a
   passenger SMS within 10 minutes of confirming the delay.
3. Passenger messages must state the route, the expected additional wait, and
   an apology. Messages must stay under 160 characters.
4. Staff must never speculate on causes that have not been confirmed by the
   operator.
""",
    "refund_policy.md": """# SLPTA Fare Refund Policy (Synthetic)

1. Refunds apply only to cancelled services, not to delays.
2. A passenger may request a refund within 48 hours with a valid ticket
   reference.
3. Refunds above 50,000 Le require supervisor approval.
4. Refunds are issued to the original payment channel where possible.
""",
    "fleet_safety_checklist.md": """# SLPTA Daily Fleet Safety Checklist (Synthetic)

Before a vehicle enters service the operator must confirm:
- Tyres have legal tread depth and correct pressure.
- Brakes, lights, and indicators are working.
- Doors open and close correctly.
- First-aid kit and fire extinguisher are present.
- Passenger capacity is not exceeded; no standing on highway routes.
""",
    "procurement_threshold_policy.md": """# SLPTA Procurement Threshold Policy (Synthetic)

1. Purchases under 5,000,000 Le may be approved by a department head.
2. Purchases from 5,000,000 to 50,000,000 Le require three written quotations.
3. Purchases above 50,000,000 Le require a tender and board approval.
4. All procurement must be recorded in the audit register within 5 working days.
""",
}

_INCIDENTS = {
    "incident_R12_2025-02-14.txt": (
        "On 14 Feb 2025 the 07:45 R12 service (Wilberforce to CBD), vehicle "
        "SLPTA-1142 under operator OP-104, departed 25 minutes late. The operator "
        "reported heavy traffic on Wilkinson Road following a stalled truck. About "
        "40 passengers were affected. Dispatch logged the cause as Traffic and "
        "issued a passenger advisory at 08:02. No injuries. Follow-up: review peak "
        "headway on the Wilberforce corridor."
    ),
    "incident_R3_2025-02-16.txt": (
        "On 16 Feb 2025 an R3 service (Waterloo to CBD) under operator OP-109 was "
        "withdrawn at Jui after a brake fault was detected during the mid-route "
        "check. 31 passengers were transferred to the following service, which "
        "added 18 minutes to their journey. Maintenance flagged the vehicle "
        "SLPTA-0907 off-service pending inspection."
    ),
}


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def ensure_course_data(seed: int = 12, force: bool = False) -> Path:
    """
    Generate the synthetic SLPTA dataset into course_data/ if it is missing.

    Returns the Path to course_data/. Safe to call at the top of every notebook;
    it is a no-op once the files exist (unless force=True).
    """
    d = data_dir()
    sentinel = d / ".version"
    already = sentinel.exists() and sentinel.read_text().strip() == DATA_VERSION
    if already and not force:
        return d

    rng = np.random.default_rng(seed)

    routes = _gen_routes()
    operators = _gen_operators(rng)
    logs = _gen_route_logs(rng, operators)
    complaints = _gen_complaints(rng)

    routes.to_csv(d / "routes.csv", index=False)
    # drop the hidden bias column before saving operators (students never see it)
    operators.drop(columns=["_bias"]).to_csv(d / "operators.csv", index=False)
    logs.to_csv(d / "route_logs.csv", index=False)
    complaints.to_csv(d / "complaints.csv", index=False)

    pol = d / "policies"
    pol.mkdir(exist_ok=True)
    for fname, body in _POLICIES.items():
        (pol / fname).write_text(body, encoding="utf-8")

    inc = d / "incident_reports"
    inc.mkdir(exist_ok=True)
    for fname, body in _INCIDENTS.items():
        (inc / fname).write_text(body, encoding="utf-8")

    sentinel.write_text(DATA_VERSION)
    return d


# ---------------------------------------------------------------------------
# Convenience loaders
# ---------------------------------------------------------------------------

def load_table(name: str) -> pd.DataFrame:
    """Load a CSV from course_data/ by stem, e.g. load_table('route_logs')."""
    ensure_course_data()
    return pd.read_csv(data_dir() / f"{name}.csv")


def load_route_logs() -> pd.DataFrame:
    return load_table("route_logs")


def load_complaints() -> pd.DataFrame:
    return load_table("complaints")


def load_routes() -> pd.DataFrame:
    return load_table("routes")


def load_operators() -> pd.DataFrame:
    return load_table("operators")


# ---------------------------------------------------------------------------
# Synthetic image set for the Day 8 transfer-learning (CNN) lab
# ---------------------------------------------------------------------------

# Three "fleet condition" classes. Each is a dominant colour + a shape, so a
# pre-trained CNN's features can separate them — while noise and jitter stop it
# being a one-pixel giveaway. Synthetic only: these are NOT photos of real buses.
_FLEET_CLASSES = {
    "roadworthy":   ((60, 160, 70),  "circle"),    # green
    "minor_faults": ((210, 160, 40), "triangle"),  # amber
    "grounded":     ((190, 55, 45),  "cross"),      # red
}


def _make_tile(rng, color, shape, size):
    """Draw one noisy, jittered synthetic condition card."""
    from PIL import Image, ImageDraw
    bg = rng.integers(120, 200, 3).tolist()
    arr = np.full((size, size, 3), bg, dtype=np.uint8)
    arr = (arr + rng.normal(0, 18, (size, size, 3))).clip(0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    draw = ImageDraw.Draw(img)
    col = tuple(int(np.clip(c + rng.normal(0, 20), 0, 255)) for c in color)
    m = size // 5
    x0 = int(rng.integers(m, size // 2)); y0 = int(rng.integers(m, size // 2))
    x1 = min(x0 + int(rng.integers(size // 3, size // 2)), size - m)
    y1 = min(y0 + int(rng.integers(size // 3, size // 2)), size - m)
    if shape == "circle":
        draw.ellipse([x0, y0, x1, y1], fill=col)
    elif shape == "triangle":
        draw.polygon([(x0, y1), ((x0 + x1) // 2, y0), (x1, y1)], fill=col)
    else:  # cross
        w = max(2, size // 10)
        draw.line([x0, y0, x1, y1], fill=col, width=w)
        draw.line([x0, y1, x1, y0], fill=col, width=w)
    return img


def ensure_fleet_images(seed: int = 7, n_train: int = 40, n_val: int = 12,
                        size: int = 96, force: bool = False) -> Path:
    """
    Generate a small synthetic fleet-condition image set for the Day 8 lab into
    course_data/fleet_images/{train,val}/{class}/*.png. Needs Pillow (in Colab).
    Returns the fleet_images/ path. No-op once generated.
    """
    base = data_dir() / "fleet_images"
    sentinel = base / ".version"
    if sentinel.exists() and sentinel.read_text().strip() == DATA_VERSION and not force:
        return base
    rng = np.random.default_rng(seed)
    for split, n in [("train", n_train), ("val", n_val)]:
        for cls, (color, shape) in _FLEET_CLASSES.items():
            d = base / split / cls
            d.mkdir(parents=True, exist_ok=True)
            for i in range(n):
                _make_tile(rng, color, shape, size).save(d / f"{cls}_{i:03d}.png")
    sentinel.write_text(DATA_VERSION)
    return base


if __name__ == "__main__":
    path = ensure_course_data(force=True)
    print(f"Course data written to: {path}")
    for csv in sorted(path.glob("*.csv")):
        df = pd.read_csv(csv)
        print(f"  {csv.name:16s} {df.shape[0]:5d} rows x {df.shape[1]} cols")
    print("Route R12 context:\n ", load_route12_context())
