const API_URL = "http://127.0.0.1:8000/predecir";

const form = document.getElementById("fraudForm");
const submitBtn = document.getElementById("submitBtn");
const clearBtn = document.getElementById("clearBtn");
const loadRiskyBtn = document.getElementById("loadRiskyBtn");
const loadSafeBtn = document.getElementById("loadSafeBtn");

const statusMessage = document.getElementById("statusMessage");
const resultSection = document.getElementById("resultSection");
const riskBanner = document.getElementById("riskBanner");

const fraudePredicho = document.getElementById("fraude_predicho");
const probabilidadFraude = document.getElementById("probabilidad_fraude");
const usuariosMismaIp = document.getElementById("usuarios_misma_ip");
const usuariosMismoDispositivo = document.getElementById("usuarios_mismo_dispositivo");
const riesgoRelacional = document.getElementById("riesgo_relacional");
const riesgoTotalText = document.getElementById("riesgo_total_text");
const riesgoTotalScore = document.getElementById("riesgo_total_score");
const summaryText = document.getElementById("summaryText");
const jsonResponse = document.getElementById("jsonResponse");
const historyTable = document.getElementById("historyTable");

let historyItems = [];

function showStatus(message, type) {
  statusMessage.textContent = message;
  statusMessage.className = `status ${type}`;
}

function hideStatus() {
  statusMessage.className = "status hidden";
  statusMessage.textContent = "";
}

function clearResults() {
  resultSection.classList.add("hidden");
  hideStatus();

  fraudePredicho.textContent = "-";
  probabilidadFraude.textContent = "-";
  usuariosMismaIp.textContent = "-";
  usuariosMismoDispositivo.textContent = "-";
  riesgoRelacional.textContent = "-";
  riesgoTotalText.textContent = "-";
  riesgoTotalScore.textContent = "-";
  summaryText.textContent = "Aquí aparecerá una interpretación general de la transacción.";
  jsonResponse.textContent = "";
  riskBanner.className = "risk-banner";
}

function setField(id, value) {
  document.getElementById(id).value = value;
}

function loadRiskyExample() {
  setField("id_usuario", 4);
  setField("edad", 25);
  setField("ingreso_mensual", 1800000);
  setField("antiguedad_cuenta_meses", 6);
  setField("num_transacciones_30d", 80);
  setField("monto_promedio", 1500000);
  setField("dispositivo_nuevo", 1);
  setField("ip_compartida", 1);
  setField("hora_madrugada", 1);
  setField("dispositivo_id", 12);
  setField("ip", "192.138.1.2");
  setField("comercio_id", 8);
}

function loadSafeExample() {
  setField("id_usuario", 9999);
  setField("edad", 38);
  setField("ingreso_mensual", 3200000);
  setField("antiguedad_cuenta_meses", 36);
  setField("num_transacciones_30d", 12);
  setField("monto_promedio", 120000);
  setField("dispositivo_nuevo", 0);
  setField("ip_compartida", 0);
  setField("hora_madrugada", 0);
  setField("dispositivo_id", 9999);
  setField("ip", "10.255.255.250");
  setField("comercio_id", 9999);
}

function getPayload() {
  return {
    id_usuario: parseInt(document.getElementById("id_usuario").value, 10),
    edad: parseInt(document.getElementById("edad").value, 10),
    ingreso_mensual: parseInt(document.getElementById("ingreso_mensual").value, 10),
    antiguedad_cuenta_meses: parseInt(document.getElementById("antiguedad_cuenta_meses").value, 10),
    num_transacciones_30d: parseInt(document.getElementById("num_transacciones_30d").value, 10),
    monto_promedio: parseInt(document.getElementById("monto_promedio").value, 10),
    dispositivo_nuevo: parseInt(document.getElementById("dispositivo_nuevo").value, 10),
    ip_compartida: parseInt(document.getElementById("ip_compartida").value, 10),
    hora_madrugada: parseInt(document.getElementById("hora_madrugada").value, 10),
    dispositivo_id: parseInt(document.getElementById("dispositivo_id").value, 10),
    ip: document.getElementById("ip").value.trim(),
    comercio_id: parseInt(document.getElementById("comercio_id").value, 10)
  };
}

function validatePayload(payload) {
  for (const [key, value] of Object.entries(payload)) {
    if (value === "" || value === null || Number.isNaN(value)) {
      return `El campo "${key}" es inválido o está vacío.`;
    }
  }

  if (!payload.ip.includes(".")) {
    return "La IP ingresada no parece válida.";
  }

  return null;
}

function buildSummary(data) {
  const fraude = data.resultado_modelo.fraude_predicho;
  const prob = data.resultado_modelo.probabilidad_fraude;
  const rel = data.resultado_grafo.riesgo_relacional;

  if (data.riesgo_total === 1) {
    return `La transacción fue clasificada como riesgosa. El modelo predictivo indicó fraude = ${fraude} con probabilidad ${prob}, y el análisis relacional devolvió riesgo = ${rel}.`;
  }

  return `La transacción fue clasificada como no riesgosa. El modelo predictivo y el análisis relacional no encontraron señales fuertes de fraude.`;
}

function renderHistory() {
  if (historyItems.length === 0) {
    historyTable.innerHTML = `
      <tr>
        <td colspan="6" class="empty-row">Aún no hay consultas realizadas.</td>
      </tr>
    `;
    return;
  }

  historyTable.innerHTML = historyItems.map(item => `
    <tr>
      <td>${item.id_usuario}</td>
      <td>${item.ip}</td>
      <td>${item.dispositivo_id}</td>
      <td><span class="pill ${item.fraude_predicho === 1 ? "red" : "green"}">${item.fraude_predicho}</span></td>
      <td><span class="pill ${item.riesgo_relacional === 1 ? "red" : "green"}">${item.riesgo_relacional}</span></td>
      <td><span class="pill ${item.riesgo_total === 1 ? "red" : "green"}">${item.riesgo_total}</span></td>
    </tr>
  `).join("");
}

function pushHistory(payload, data) {
  historyItems.unshift({
    id_usuario: payload.id_usuario,
    ip: payload.ip,
    dispositivo_id: payload.dispositivo_id,
    fraude_predicho: data.resultado_modelo.fraude_predicho,
    riesgo_relacional: data.resultado_grafo.riesgo_relacional,
    riesgo_total: data.riesgo_total
  });

  if (historyItems.length > 8) {
    historyItems = historyItems.slice(0, 8);
  }

  renderHistory();
}

function renderResult(data) {
  fraudePredicho.textContent = data.resultado_modelo.fraude_predicho;
  probabilidadFraude.textContent = data.resultado_modelo.probabilidad_fraude;
  usuariosMismaIp.textContent = data.resultado_grafo.usuarios_misma_ip;
  usuariosMismoDispositivo.textContent = data.resultado_grafo.usuarios_mismo_dispositivo;
  riesgoRelacional.textContent = data.resultado_grafo.riesgo_relacional;
  riesgoTotalScore.textContent = data.riesgo_total;
  jsonResponse.textContent = JSON.stringify(data, null, 2);
  summaryText.textContent = buildSummary(data);

  if (data.riesgo_total === 1) {
    riesgoTotalText.textContent = "Riesgo alto";
    riskBanner.className = "risk-banner high";
    showStatus("Transacción clasificada como riesgosa.", "error");
  } else {
    riesgoTotalText.textContent = "Riesgo bajo";
    riskBanner.className = "risk-banner low";
    showStatus("Transacción clasificada como no riesgosa.", "success");
  }

  resultSection.classList.remove("hidden");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = getPayload();
  const validationError = validatePayload(payload);

  if (validationError) {
    showStatus(validationError, "error");
    return;
  }

  showStatus("Consultando la API principal...", "loading");
  resultSection.classList.add("hidden");
  submitBtn.disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Ocurrió un error consumiendo la API.");
    }

    renderResult(data);
    pushHistory(payload, data);
  } catch (error) {
    showStatus(`Error: ${error.message}`, "error");
  } finally {
    submitBtn.disabled = false;
  }
});

clearBtn.addEventListener("click", () => {
  clearResults();
  form.reset();
});

loadRiskyBtn.addEventListener("click", loadRiskyExample);
loadSafeBtn.addEventListener("click", loadSafeExample);

renderHistory();
loadRiskyExample();