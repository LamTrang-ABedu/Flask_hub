let accountData = [];

async function loadAccounts() {
  const res = await fetch('/api/account-fetcher');
  const data = await res.json();
  if (data.status !== 'ok') {
    alert('Error loading accounts: ' + data.message);
    return;
  }

  accountData = data.accounts;
  renderAccounts(accountData);
}

function renderAccounts(list) {
  const table = document.getElementById('accountTable');
  const tbody = table.querySelector('tbody');
  tbody.innerHTML = '';

  list.forEach(acc => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${acc.username}</td>
      <td>${acc.password}</td>
      <td>${acc.source}</td>
      <td>${acc.category}</td>
      <td>
        <button onclick="copyText('${acc.username}:${acc.password}')">Copy</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  table.style.display = list.length ? 'table' : 'none';
}

function filterAccounts() {
  const search = document.getElementById('searchInput').value.toLowerCase();
  const category = document.getElementById('filterSelect').value;

  const filtered = accountData.filter(acc => {
    return (
      (acc.username.toLowerCase().includes(search) || acc.source.toLowerCase().includes(search)) &&
      (category === '' || acc.category === category)
    );
  });

  renderAccounts(filtered);
}

function copyText(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert('Copied: ' + text);
  });
}
