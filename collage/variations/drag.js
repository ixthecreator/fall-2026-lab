// The photos and nodes are already in the HTML. This file only handles movement.
const svg = document.querySelector(".artwork");
const config = JSON.parse(document.querySelector("#composition").textContent);
const status = document.querySelector('[role="status"]');
const nodes = new Map(
  config.nodes.map((node) => [
    String(node.id),
    { ...node, homeX: node.x, homeY: node.y },
  ]),
);
const dots = [...svg.querySelectorAll("[data-node]")];
const lines = [...svg.querySelectorAll("[data-a]")];
const pieces = [...svg.querySelectorAll("[data-feature]")].map((element) => ({
  element,
  id: element.dataset.feature,
  x: 0,
  y: 0,
}));
let active = null;
let frame = null;

function draw() {
  frame = null;
  for (const piece of pieces)
    piece.element.setAttribute("transform", `translate(${piece.x} ${piece.y})`);
  for (const dot of dots) {
    const node = nodes.get(dot.dataset.node);
    dot.setAttribute("cx", node.x);
    dot.setAttribute("cy", node.y);
  }
  for (const line of lines) {
    const a = nodes.get(line.dataset.a);
    const b = nodes.get(line.dataset.b);
    line.setAttribute("x1", a.x);
    line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x);
    line.setAttribute("y2", b.y);
  }
}
function move(piece, x, y) {
  const box = config.bounds[piece.id];
  x = Math.max(12 - box.x, Math.min(988 - box.x - box.w, x));
  y = Math.max(12 - box.y, Math.min(1088 - box.y - box.h, y));
  const dx = x - piece.x,
    dy = y - piece.y;
  piece.x = x;
  piece.y = y;
  for (const id of config.attachments[piece.id]) {
    const node = nodes.get(String(id));
    node.x += dx;
    node.y += dy;
  }
  if (!frame) frame = requestAnimationFrame(draw);
}
function point(event) {
  return new DOMPoint(event.clientX, event.clientY).matrixTransform(
    svg.getScreenCTM().inverse(),
  );
}
function release() {
  if (!active) return;
  if (active.piece.element.hasPointerCapture(active.pointer))
    active.piece.element.releasePointerCapture(active.pointer);
  active = null;
}
function reset() {
  release();
  for (const piece of pieces) {
    piece.x = 0;
    piece.y = 0;
  }
  for (const node of nodes.values()) {
    node.x = node.homeX;
    node.y = node.homeY;
  }
  if (frame) cancelAnimationFrame(frame);
  draw();
  status.textContent = "Original collage restored.";
}
for (const piece of pieces) {
  piece.element.addEventListener("pointerdown", (event) => {
    if (event.button !== 0 || active) return;
    event.preventDefault();
    piece.element.focus({ preventScroll: true });
    const start = point(event);
    active = { piece, pointer: event.pointerId, start, x: piece.x, y: piece.y };
    piece.element.setPointerCapture(event.pointerId);
    svg.querySelector(".features").append(piece.element);
  });
  piece.element.addEventListener("pointermove", (event) => {
    if (!active || event.pointerId !== active.pointer) return;
    const current = point(event);
    move(
      piece,
      active.x + current.x - active.start.x,
      active.y + current.y - active.start.y,
    );
  });
  piece.element.addEventListener("pointerup", release);
  piece.element.addEventListener("pointercancel", release);
  piece.element.addEventListener("lostpointercapture", () => {
    active = null;
  });
  piece.element.addEventListener("keydown", (event) => {
    const directions = {
      ArrowLeft: [-1, 0],
      ArrowRight: [1, 0],
      ArrowUp: [0, -1],
      ArrowDown: [0, 1],
    };
    if (!directions[event.key]) return;
    event.preventDefault();
    const [dx, dy] = directions[event.key],
      step = event.shiftKey ? 20 : 5;
    move(piece, piece.x + dx * step, piece.y + dy * step);
    status.textContent = `${piece.id.replaceAll("-", " ")} moved.`;
  });
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") reset();
});
