import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_URL = "https://pokeapi.co/api/v2"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def fetch(path: str, params: dict = None):
    """Forward a GET request to PokéAPI and return parsed JSON.

    Raises:
        HTTPError responses are caught and returned as JSON error objects
        with the upstream status code preserved.
    """
    try:
        response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else 502
        message = f"PokéAPI error: {exc.response.text}" if exc.response is not None else str(exc)
        return {"error": message}, status
    except requests.exceptions.Timeout:
        return {"error": "PokéAPI request timed out"}, 504
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}, 502


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Simple liveness probe."""
    return jsonify({"status": "ok"}), 200


# ---------------------------------------------------------------------------
# Pokémon
# ---------------------------------------------------------------------------

@app.route("/pokemon", methods=["GET"])
def list_pokemon():
    """List pokémon with optional pagination.

    Query params:
        limit  (int, default 20)
        offset (int, default 0)
    """
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))
    data, status = fetch("/pokemon", params={"limit": limit, "offset": offset})
    return jsonify(data), status


@app.route("/pokemon/<name_or_id>", methods=["GET"])
def get_pokemon(name_or_id: str):
    """Get details for a single Pokémon by name or national-dex ID."""
    data, status = fetch(f"/pokemon/{name_or_id.lower()}")
    return jsonify(data), status


@app.route("/pokemon/<name_or_id>/abilities", methods=["GET"])
def get_pokemon_abilities(name_or_id: str):
    """Get the abilities of a single Pokémon."""
    data, status = fetch(f"/pokemon/{name_or_id.lower()}")
    if status != 200:
        return jsonify(data), status
    abilities = [
        {
            "name": a["ability"]["name"],
            "is_hidden": a["is_hidden"],
            "slot": a["slot"],
        }
        for a in data.get("abilities", [])
    ]
    return jsonify({"pokemon": data["name"], "abilities": abilities}), 200


@app.route("/pokemon/<name_or_id>/moves", methods=["GET"])
def get_pokemon_moves(name_or_id: str):
    """Get the move list of a single Pokémon."""
    data, status = fetch(f"/pokemon/{name_or_id.lower()}")
    if status != 200:
        return jsonify(data), status
    moves = [m["move"]["name"] for m in data.get("moves", [])]
    return jsonify({"pokemon": data["name"], "moves": moves}), 200


@app.route("/pokemon/<name_or_id>/stats", methods=["GET"])
def get_pokemon_stats(name_or_id: str):
    """Get the base stats of a single Pokémon."""
    data, status = fetch(f"/pokemon/{name_or_id.lower()}")
    if status != 200:
        return jsonify(data), status
    stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}
    return jsonify({"pokemon": data["name"], "stats": stats}), 200


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@app.route("/type", methods=["GET"])
def list_types():
    """List all Pokémon types."""
    data, status = fetch("/type")
    return jsonify(data), status


@app.route("/type/<name_or_id>", methods=["GET"])
def get_type(name_or_id: str):
    """Get details for a specific type (damage relations, pokémon list, etc.)."""
    data, status = fetch(f"/type/{name_or_id.lower()}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Abilities
# ---------------------------------------------------------------------------

@app.route("/ability", methods=["GET"])
def list_abilities():
    """List all abilities with optional pagination.

    Query params:
        limit  (int, default 20)
        offset (int, default 0)
    """
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))
    data, status = fetch("/ability", params={"limit": limit, "offset": offset})
    return jsonify(data), status


@app.route("/ability/<name_or_id>", methods=["GET"])
def get_ability(name_or_id: str):
    """Get details for a specific ability."""
    data, status = fetch(f"/ability/{name_or_id.lower()}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Moves
# ---------------------------------------------------------------------------

@app.route("/move", methods=["GET"])
def list_moves():
    """List all moves with optional pagination.

    Query params:
        limit  (int, default 20)
        offset (int, default 0)
    """
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))
    data, status = fetch("/move", params={"limit": limit, "offset": offset})
    return jsonify(data), status


@app.route("/move/<name_or_id>", methods=["GET"])
def get_move(name_or_id: str):
    """Get details for a specific move."""
    data, status = fetch(f"/move/{name_or_id.lower()}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Generations
# ---------------------------------------------------------------------------

@app.route("/generation", methods=["GET"])
def list_generations():
    """List all Pokémon generations."""
    data, status = fetch("/generation")
    return jsonify(data), status


@app.route("/generation/<name_or_id>", methods=["GET"])
def get_generation(name_or_id: str):
    """Get details for a specific generation."""
    data, status = fetch(f"/generation/{name_or_id.lower()}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Species
# ---------------------------------------------------------------------------

@app.route("/pokemon-species/<name_or_id>", methods=["GET"])
def get_species(name_or_id: str):
    """Get species data for a Pokémon (flavor texts, evolution chain URL, etc.)."""
    data, status = fetch(f"/pokemon-species/{name_or_id.lower()}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Evolution chains
# ---------------------------------------------------------------------------

@app.route("/evolution-chain/<string:chain_id>", methods=["GET"])
def get_evolution_chain(chain_id: str):
    """Get a full evolution chain by its numeric ID."""
    data, status = fetch(f"/evolution-chain/{chain_id}")
    return jsonify(data), status


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug, port=5000)
