const R2_BASE = "https://lam.io.vn/MEDIA/";

async function loadGallery() {
  const source = document.getElementById('sourceSelect').value;
  const grid = document.getElementById('mediaGrid');
  grid.innerHTML = '<p>Loading...</p>';

  if (!source) {
    grid.innerHTML = '<p>Please select a source.</p>';
    return;
  }

  const r2Url = `${R2_BASE}/${source}/media.json`;
  try {
    const res = await fetch(r2Url);
    const data = await res.json();

    grid.innerHTML = '';
    data.results.forEach(item => {
      const card = document.createElement('div');
      card.className = 'media-card';

      if (item.type === 'video') {
        card.innerHTML = `
          <div class="thumb" onclick="openViewer('${item.video}', 'video')">
            <img src="${item.thumb}" alt="${item.title}" />
            <div class="play-icon">&#9658;</div>
          </div>
          <p>${item.title}</p>
        `;
      } else {
        card.innerHTML = `
          <div class="thumb" onclick="openViewer('${item.image}', 'image')">
            <img src="${item.image}" alt="${item.title}" />
          </div>
          <p>${item.title}</p>
        `;
      }
      grid.appendChild(card);
    });
  } catch (e) {
    console.error(e);
    grid.innerHTML = '<p style="color:red;">Failed to load gallery.</p>';
  }
}

function openViewer(src, type) {
  const modal = document.getElementById('modalViewer');
  const modalImg = document.getElementById('modalImage');
  const modalVideo = document.getElementById('modalVideo');

  if (type === 'image') {
    modalImg.src = src;
    modalImg.style.display = 'block';
    modalVideo.style.display = 'none';
  } else {
    modalVideo.src = src;
    modalVideo.style.display = 'block';
    modalImg.style.display = 'none';
  }
  modal.style.display = 'block';
}

function closeViewer() {
  const modal = document.getElementById('modalViewer');
  modal.style.display = 'none';
  document.getElementById('modalImage').src = '';
  document.getElementById('modalVideo').src = '';
}
