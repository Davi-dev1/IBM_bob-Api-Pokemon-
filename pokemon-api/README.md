# Pokémon REST API

A lightweight **read-only** REST wrapper around [PokéAPI](https://pokeapi.co) built with Flask.  
All endpoints use **GET** only — no authentication required.

---

## Getting started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the development server
python app.py
```

The server starts at `http://localhost:5000`.

---

## Endpoints

### Pokémon

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pokemon` | List pokémon (supports `?limit=` & `?offset=`) |
| GET | `/pokemon/<name_or_id>` | Full details for a single Pokémon |
| GET | `/pokemon/<name_or_id>/abilities` | Abilities of a Pokémon |
| GET | `/pokemon/<name_or_id>/moves` | Move list of a Pokémon |
| GET | `/pokemon/<name_or_id>/stats` | Base stats of a Pokémon |

### Types

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/type` | List all types |
| GET | `/type/<name_or_id>` | Details for a specific type (damage relations, etc.) |

### Abilities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ability` | List abilities (supports `?limit=` & `?offset=`) |
| GET | `/ability/<name_or_id>` | Details for a specific ability |

### Moves

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/move` | List moves (supports `?limit=` & `?offset=`) |
| GET | `/move/<name_or_id>` | Details for a specific move |

### Generations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/generation` | List all generations |
| GET | `/generation/<name_or_id>` | Details for a specific generation |

### Species & Evolution

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pokemon-species/<name_or_id>` | Species data (flavor texts, evolution chain URL, etc.) |
| GET | `/evolution-chain/<chain_id>` | Full evolution chain by numeric ID |

---

## Examples

```bash
# Get Pikachu
curl http://localhost:5000/pokemon/pikachu

# Get Pikachu's stats
curl http://localhost:5000/pokemon/pikachu/stats

# List first 5 pokémon
curl "http://localhost:5000/pokemon?limit=5&offset=0"

# Get fire type details
curl http://localhost:5000/type/fire

# Get evolution chain #1 (Bulbasaur line)
curl http://localhost:5000/evolution-chain/1
```

---

## Response format

All responses are **JSON** proxied directly from [PokéAPI v2](https://pokeapi.co/docs/v2).  
Convenience endpoints (`/abilities`, `/moves`, `/stats`) return a simplified subset.

---

## Tech stack

| Dependency | Version |
|------------|---------|
| Python | ≥ 3.9 |
| Flask | ≥ 3.0 |
| Requests | ≥ 2.31 |

---

## License

MIT
