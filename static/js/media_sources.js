
async function loadGallery() {
  const source = document.getElementById('sourceSelect').value;
  const grid = document.getElementById('mediaGrid');
  grid.innerHTML = '<p>Loading...</p>';
  const res = await fetch(`/api/gallery?source=${source}`);
  const data = await res.json();
  grid.innerHTML = '';
  if (data.status !== 'ok') {
    grid.innerHTML = `<p style="color:red;">${data.message}</p>`;
    return;
  }
  data.results.forEach(item => {
    const card = document.createElement('div');
    card.className = 'media-card';
    card.innerHTML = `
      <div class="thumb lozad" data-background-image="${item.thumb}"></div>
      <p>${item.title}</p>
      <a href="${item.video}" target="_blank">Watch</a>
    `;
    grid.appendChild(card);
  });
  const observer = lozad('.lozad');
  observer.observe();
}
