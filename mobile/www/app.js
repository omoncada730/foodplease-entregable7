const DEFAULT_BACKEND = "http://10.0.2.2:5000";
const STORAGE_KEY = "foodplease.backendUrl";

function getBackend() {
    return localStorage.getItem(STORAGE_KEY) || DEFAULT_BACKEND;
}

function setStatus(text, kind) {
    const el = document.getElementById("status");
    el.textContent = text;
    el.className = kind || "";
}

async function fetchJson(path) {
    const url = getBackend() + path;
    const res = await fetch(url, { headers: { Accept: "application/json" } });
    if (!res.ok) throw new Error("HTTP " + res.status);
    return res.json();
}

function renderProductos(items) {
    const ul = document.getElementById("productos");
    ul.innerHTML = "";
    items.slice(0, 5).forEach((p) => {
        const li = document.createElement("li");
        li.innerHTML = `<span>${p.nombre}</span><strong>$${p.precio}</strong>`;
        ul.appendChild(li);
    });
    if (items.length === 0) ul.innerHTML = "<li>(sin productos)</li>";
}

function renderPedidos(items) {
    const ul = document.getElementById("pedidos");
    ul.innerHTML = "";
    items.slice(0, 5).forEach((p) => {
        const li = document.createElement("li");
        li.innerHTML = `<span>#${p.id} · ${p.cliente_nombre || "-"}</span><strong>${p.estado}</strong>`;
        ul.appendChild(li);
    });
    if (items.length === 0) ul.innerHTML = "<li>(sin pedidos)</li>";
}

async function refresh() {
    setStatus("Cargando datos del backend...");
    try {
        const [productos, pedidos] = await Promise.all([
            fetchJson("/api/productos"),
            fetchJson("/api/pedidos"),
        ]);
        renderProductos(productos);
        renderPedidos(pedidos);
        setStatus("Conectado a " + getBackend(), "ok");
    } catch (e) {
        setStatus("Error: " + e.message + " (backend: " + getBackend() + ")", "error");
    }
}

document.getElementById("default-url").textContent = DEFAULT_BACKEND;
document.getElementById("backend-url").value = getBackend();

document.getElementById("btn-save").addEventListener("click", () => {
    const val = document.getElementById("backend-url").value.trim();
    if (val) localStorage.setItem(STORAGE_KEY, val);
    refresh();
});

document.getElementById("btn-open-web").addEventListener("click", () => {
    window.location.href = getBackend() + "/";
});

document.querySelectorAll(".bottom-nav a").forEach((a) => {
    a.addEventListener("click", (e) => {
        e.preventDefault();
        const action = a.dataset.action;
        if (action === "reload") refresh();
        if (action === "open") window.location.href = getBackend() + "/";
        if (action === "api") window.location.href = getBackend() + "/api/productos";
    });
});

refresh();
