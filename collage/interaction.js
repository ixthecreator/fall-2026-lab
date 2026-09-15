// Source coordinates refer to the gallery photograph (749 × 1000).
const artwork = document.querySelector(".artwork");
const features = [...artwork.querySelectorAll(".feature")];
const connections = artwork.querySelector(".connections");
const status = document.querySelector(".status");
const state = features.map((element) => ({
  element,
  homeX: Number(element.getAttribute("x")),
  homeY: Number(element.getAttribute("y")),
  width: Number(element.getAttribute("width")),
  height: Number(element.getAttribute("height")),
  x: Number(element.getAttribute("x")),
  y: Number(element.getAttribute("y")),
  hole: artwork.querySelector(`[data-hole="${element.dataset.feature}"]`),
}));
let active = null;

function draw() {
  connections.replaceChildren();
  for (const item of state) {
    item.element.setAttribute("x", item.x);
    item.element.setAttribute("y", item.y);
    const moved =
      Math.abs(item.x - item.homeX) + Math.abs(item.y - item.homeY) > 0.5;
    item.hole.setAttribute("opacity", moved ? "1" : "0");
    if (!moved) continue;
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    const points = {
      x1: item.homeX + item.width / 2,
      y1: item.homeY + item.height / 2,
      x2: item.x + item.width / 2,
      y2: item.y + item.height / 2,
    };
    for (const [name, value] of Object.entries(points))
      line.setAttribute(name, value);
    connections.append(line);
  }
}
function move(item, x, y) {
  item.x = Math.max(0, Math.min(749 - item.width, x));
  item.y = Math.max(0, Math.min(1000 - item.height, y));
  draw();
}
function restore() {
  active = null;
  for (const item of state) {
    item.x = item.homeX;
    item.y = item.homeY;
  }
  draw();
  status.textContent = "Original arrangement restored.";
}
for (const item of state) {
  const element = item.element;
  element.addEventListener("pointerdown", (event) => {
    if (event.button !== 0 || active) return;
    element.focus({ preventScroll: true });
    artwork.append(element);
    const rect = artwork.getBoundingClientRect();
    active = {
      item,
      pointer: event.pointerId,
      startX: event.clientX,
      startY: event.clientY,
      x: item.x,
      y: item.y,
      scaleX: 749 / rect.width,
      scaleY: 1000 / rect.height,
    };
    element.setPointerCapture(event.pointerId);
  });
  element.addEventListener("pointermove", (event) => {
    if (!active || active.item !== item || active.pointer !== event.pointerId)
      return;
    move(
      item,
      active.x + (event.clientX - active.startX) * active.scaleX,
      active.y + (event.clientY - active.startY) * active.scaleY,
    );
  });
  const release = (event) => {
    if (!active || active.pointer !== event.pointerId) return;
    active = null;
    status.textContent =
      element.getAttribute("aria-label").replace("Move ", "") + " moved.";
  };
  element.addEventListener("pointerup", release);
  element.addEventListener("pointercancel", release);
  element.addEventListener("lostpointercapture", release);
  element.addEventListener("keydown", (event) => {
    const direction = {
      ArrowLeft: [-1, 0],
      ArrowRight: [1, 0],
      ArrowUp: [0, -1],
      ArrowDown: [0, 1],
    }[event.key];
    if (!direction) return;
    event.preventDefault();
    artwork.append(element);
    const step = event.shiftKey ? 20 : 5;
    move(item, item.x + direction[0] * step, item.y + direction[1] * step);
    status.textContent =
      element.getAttribute("aria-label").replace("Move ", "") + " moved.";
  });
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") restore();
});
draw();
