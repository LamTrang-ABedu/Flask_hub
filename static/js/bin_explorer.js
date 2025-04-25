
let binData = [];

async function fetchBINs() {
  const res = await fetch("/api/bin");
  const data = await res.json();
  binData = data;
  populateCountries(data);
  renderTable(data);
}

function populateCountries(data) {
  const select = document.getElementById('countrySelect');
  const countries = [...new Set(data.map(x => x.country))].sort();
  select.innerHTML = '<option value="">-- All --</option>';
  countries.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c;
    select.appendChild(opt);
  });
}

function filterBINs() {
  const ctry = document.getElementById('countrySelect').value;
  const filtered = ctry ? binData.filter(x => x.country === ctry) : binData;
  renderTable(filtered);
}

function renderTable(data) {
  const tbody = document.querySelector('#binTable tbody');
  tbody.innerHTML = '';
  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${row.bin}</td><td>${row.brand}</td><td>${row.bank}</td><td>${row.type}</td><td>${row.country}</td>`;
    tbody.appendChild(tr);
  });
}

function exportJSON() {
  const ctry = document.getElementById('countrySelect').value;
  const filtered = ctry ? binData.filter(x => x.country === ctry) : binData;
  const blob = new Blob([JSON.stringify(filtered, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "binlist.json";
  a.click();
}

window.onload = fetchBINs;
