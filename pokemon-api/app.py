from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

BASE_URL = "https://pokeapi.co/api/v2"


def fetch(path: str, params: dict = None):
    """Helper: forward a GET request to PokéAPI and return parsed JSON."""
    response = requests.get(f"{BASE_URL}{path}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


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
    limit = request.args.get("limit", 20)
    offset = request.args.get("offset", 0)
    data = fetch("/pokemon", params={"limit": limit, "offset": offset})
    return jsonify(data)


@app.route("/pokemon/<name_or_id>", methods=["GET"])
def get_pokemon(name_or_id: str):
    """Get details for a single Pokémon by name or national-dex ID."""
    data = fetch(f"/pokemon/{name_or_id.lower()}")
    return jsonify(data)


@app.route("/pokemon/<name_or_id>/abilities", methods=["GET"])
def get_pokemon_abilities(name_or_id: str):
    """Get the abilities of a single Pokémon."""
    data = fetch(f"/pokemon/{name_or_id.lower()}")
    abilities = [
        {
            "name": a["ability"]["name"],
            "is_hidden": a["is_hidden"],
            "slot": a["slot"],
        }
        for a in data.get("abilities", [])
    ]
    return jsonify({"pokemon": data["name"], "abilities": abilities})


@app.route("/pokemon/<name_or_id>/moves", methods=["GET"])
def get_pokemon_moves(name_or_id: str):
    """Get the move list of a single Pokémon."""
    data = fetch(f"/pokemon/{name_or_id.lower()}")
    moves = [m["move"]["name"] for m in data.get("moves", [])]
    return jsonify({"pokemon": data["name"], "moves": moves})


@app.route("/pokemon/<name_or_id>/stats", methods=["GET"])
def get_pokemon_stats(name_or_id: str):
    """Get the base stats of a single Pokémon."""
    data = fetch(f"/pokemon/{name_or_id.lower()}")
    stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}
    return jsonify({"pokemon": data["name"], "stats": stats})


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

@app.route("/type", methods=["GET"])
def list_types():
    """List all Pokémon types."""
    data = fetch("/type")
    return jsonify(data)


@app.route("/type/<name_or_id>", methods=["GET"])
def get_type(name_or_id: str):
    """Get details for a specific type (damage relations, pokémon list, etc.)."""
    data = fetch(f"/type/{name_or_id.lower()}")
    return jsonify(data)


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
    limit = request.args.get("limit", 20)
    offset = request.args.get("offset", 0)
    data = fetch("/ability", params={"limit": limit, "offset": offset})
    return jsonify(data)


@app.route("/ability/<name_or_id>", methods=["GET"])
def get_ability(name_or_id: str):
    """Get details for a specific ability."""
    data = fetch(f"/ability/{name_or_id.lower()}")
    return jsonify(data)


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
    limit = request.args.get("limit", 20)
    offset = request.args.get("offset", 0)
    data = fetch("/move", params={"limit": limit, "offset": offset})
    return jsonify(data)


@app.route("/move/<name_or_id>", methods=["GET"])
def get_move(name_or_id: str):
    """Get details for a specific move."""
    data = fetch(f"/move/{name_or_id.lower()}")
    return jsonify(data)


# ---------------------------------------------------------------------------
# Generations
# ---------------------------------------------------------------------------

@app.route("/generation", methods=["GET"])
def list_generations():
    """List all Pokémon generations."""
    data = fetch("/generation")
    return jsonify(data)


@app.route("/generation/<name_or_id>", methods=["GET"])
def get_generation(name_or_id: str):
    """Get details for a specific generation."""
    data = fetch(f"/generation/{name_or_id.lower()}")
    return jsonify(data)


# ---------------------------------------------------------------------------
# Species
# ---------------------------------------------------------------------------

@app.route("/pokemon-species/<name_or_id>", methods=["GET"])
def get_species(name_or_id: str):
    """Get species data for a Pokémon (flavor texts, evolution chain URL, etc.)."""
    data = fetch(f"/pokemon-species/{name_or_id.lower()}")
    return jsonify(data)


# ---------------------------------------------------------------------------
# Evolution chains
# ---------------------------------------------------------------------------

@app.route("/evolution-chain/<chain_id>", methods=["GET"])
def get_evolution_chain(chain_id: int):
    """Get a full evolution chain by its numeric ID."""
    data = fetch(f"/evolution-chain/{chain_id}")
    return jsonify(data)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
