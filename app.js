const MAX_POKEMON_ID = 1025;
const POKEMON_COUNT = 3;
const API_BASE = "https://pokeapi.co/api/v2/pokemon";

const listEl = document.getElementById("pokemon-list");
const reloadBtn = document.getElementById("reload-btn");

function pickRandomIds(count, max) {
  const ids = new Set();
  while (ids.size < count) {
    ids.add(Math.floor(Math.random() * max) + 1);
  }
  return [...ids];
}

async function fetchPokemon(id) {
  const res = await fetch(`${API_BASE}/${id}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch Pokemon #${id}: ${res.status}`);
  }
  return res.json();
}

function getSpriteUrl(pokemon) {
  const sprites = pokemon.sprites;
  return (
    sprites?.other?.["official-artwork"]?.front_default ||
    sprites?.front_default ||
    ""
  );
}

function renderSkeletons() {
  listEl.innerHTML = "";
  for (let i = 0; i < POKEMON_COUNT; i++) {
    const div = document.createElement("div");
    div.className = "skeleton";
    div.textContent = "読み込み中...";
    listEl.appendChild(div);
  }
}

function renderError(message) {
  listEl.innerHTML = "";
  const div = document.createElement("div");
  div.className = "error";
  div.textContent = message;
  listEl.appendChild(div);
}

function renderPokemon(pokemons) {
  listEl.innerHTML = "";
  for (const p of pokemons) {
    const card = document.createElement("article");
    card.className = "pokemon-card";

    const sprite = getSpriteUrl(p);
    const types = p.types
      .map(
        (t) =>
          `<span class="type-badge type-${t.type.name}">${t.type.name}</span>`,
      )
      .join("");

    card.innerHTML = `
      <img src="${sprite}" alt="${p.name}" loading="lazy" />
      <p class="pokemon-id">No. ${String(p.id).padStart(4, "0")}</p>
      <h2 class="pokemon-name">${p.name}</h2>
      <div class="pokemon-types">${types}</div>
      <div class="pokemon-meta">
        <span>身長: ${(p.height / 10).toFixed(1)} m</span>
        <span>体重: ${(p.weight / 10).toFixed(1)} kg</span>
      </div>
    `;
    listEl.appendChild(card);
  }
}

async function loadRandomPokemon() {
  reloadBtn.disabled = true;
  renderSkeletons();
  try {
    const ids = pickRandomIds(POKEMON_COUNT, MAX_POKEMON_ID);
    const pokemons = await Promise.all(ids.map(fetchPokemon));
    renderPokemon(pokemons);
  } catch (err) {
    console.error(err);
    renderError("ポケモンの取得に失敗しました。もう一度お試しください。");
  } finally {
    reloadBtn.disabled = false;
  }
}

reloadBtn.addEventListener("click", loadRandomPokemon);
loadRandomPokemon();
