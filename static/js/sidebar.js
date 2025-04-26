
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  sb.style.width = sb.style.width === "220px" ? "0" : "220px";
}
function closeSidebar() {
  const sb = document.getElementById("sidebar");
  if (window.innerWidth < 768) sb.style.width = "0";
}
document.addEventListener('click', function(event) {
  const sb = document.getElementById("sidebar");
  const toggle = document.querySelector('.topbar');

  // Nếu click không nằm trong sidebar hoặc toggle button
  if (!sb.contains(event.target) && !toggle.contains(event.target)) {
    sb.style.width = "0";
  }
});

