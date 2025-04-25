
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  sb.style.width = sb.style.width === "220px" ? "0" : "220px";
}
function closeSidebar() {
  const sb = document.getElementById("sidebar");
  if (window.innerWidth < 768) sb.style.width = "0";
}
