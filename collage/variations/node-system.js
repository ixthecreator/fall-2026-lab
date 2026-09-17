import { createMesh } from "./mesh-model.mjs";
const svg = document.querySelector(".artwork");
const config = JSON.parse(document.querySelector("#composition").textContent);
const mesh = createMesh(config.nodes, config.edges);
const network = svg.querySelector(":scope > .network");
const dots = [...network.querySelectorAll("[data-node]")];
const lines = [...network.querySelectorAll("[data-a]")];
const handles = [...svg.querySelectorAll("[data-handle]")];
const pieces = [...svg.querySelectorAll("[data-feature]")];
const traces = svg.querySelector(".gesture-traces");
const status = document.querySelector('[role="status"]');
const reduced = matchMedia("(prefers-reduced-motion: reduce)");
let active = null,
  recovery = null,
  recoveryFrame = null,
  keyTimer = null;
const history = [];
const point = (event) =>
  new DOMPoint(event.clientX, event.clientY).matrixTransform(
    svg.getScreenCTM().inverse(),
  );
const getNode = (id) => mesh.points[mesh.byId.get(String(id))];
function draw() {
  dots.forEach((dot) => {
    const n = getNode(dot.dataset.node);
    dot.setAttribute("cx", n.x);
    dot.setAttribute("cy", n.y);
    dot.setAttribute(
      "r",
      Math.min(4, 1.3 + Math.hypot(n.x - n.homeX, n.y - n.homeY) / 25),
    );
  });
  handles.forEach((h) => {
    const n = getNode(h.dataset.handle);
    h.setAttribute("cx", n.x);
    h.setAttribute("cy", n.y);
  });
  lines.forEach((line, i) => {
    const { i: a, j: b, length } = mesh.links[i];
    const p = mesh.points[a],
      q = mesh.points[b];
    const strain = Math.min(
      1,
      Math.abs(Math.hypot(p.x - q.x, p.y - q.y) / length - 1),
    );
    line.setAttribute("x1", p.x);
    line.setAttribute("y1", p.y);
    line.setAttribute("x2", q.x);
    line.setAttribute("y2", q.y);
    line.setAttribute("stroke", strain > 0.25 ? "#ecff91" : "#e9da72");
    line.setAttribute("stroke-width", 0.65 + strain * 2.2);
  });
  pieces.forEach((piece) => {
    const ids = config.attachments[piece.dataset.feature];
    const region = ids.map(getNode);
    const dx =
      region.reduce((sum, n) => sum + n.x - n.homeX, 0) / region.length;
    const dy =
      region.reduce((sum, n) => sum + n.y - n.homeY, 0) / region.length;
    const box = config.bounds[piece.dataset.feature];
    const x = Math.max(12 - box.x, Math.min(988 - box.x - box.w, dx));
    const y = Math.max(12 - box.y, Math.min(1088 - box.y - box.h, dy));
    piece.setAttribute("transform", `translate(${x} ${y})`);
    // The measured region selects how much of the second borrowed image appears.
    piece
      .querySelector(".alternate-image")
      .setAttribute("opacity", Math.min(0.95, Math.hypot(dx, dy) / 100));
  });
  for (const trace of history) {
    const n = getNode(trace.id);
    trace.line.setAttribute("x2", n.x);
    trace.line.setAttribute("y2", n.y);
  }
}
function stopRecovery() {
  clearTimeout(keyTimer);
  if (recoveryFrame) cancelAnimationFrame(recoveryFrame);
  recoveryFrame = null;
  recovery = null;
}
function beginRecovery() {
  const start = mesh.snapshot();
  if (reduced.matches) {
    mesh.restore(start, 0.35);
    draw();
    return;
  }
  recovery = { start, time: performance.now() };
  function tick(now) {
    if (!recovery) return;
    const t = Math.min(1, (now - recovery.time) / 1400);
    const eased = 1 - (1 - t) ** 3;
    mesh.restore(recovery.start, 1 - 0.65 * eased);
    draw();
    if (t < 1) recoveryFrame = requestAnimationFrame(tick);
    else {
      recovery = null;
      recoveryFrame = null;
    }
  }
  recoveryFrame = requestAnimationFrame(tick);
}
function remember(id) {
  const n = getNode(id),
    ns = "http://www.w3.org/2000/svg";
  const group = document.createElementNS(ns, "g");
  const line = document.createElementNS(ns, "line");
  line.setAttribute("x1", n.x);
  line.setAttribute("y1", n.y);
  const circle = document.createElementNS(ns, "circle");
  circle.setAttribute("cx", n.x);
  circle.setAttribute("cy", n.y);
  circle.setAttribute("r", 8);
  group.append(line, circle);
  traces.append(group);
  history.push({ id, line, group });
  if (history.length > 12) history.shift().group.remove();
}
function nearest(p, candidates = mesh.points) {
  return candidates.reduce((a, b) =>
    Math.hypot(a.x - p.x, a.y - p.y) < Math.hypot(b.x - p.x, b.y - p.y) ? a : b,
  );
}
svg.addEventListener("pointerdown", (event) => {
  if (event.button !== 0 || active) return;
  const p = point(event),
    feature = event.target.closest("[data-feature]");
  const selected = nearest(
    p,
    feature
      ? config.attachments[feature.dataset.feature].map(getNode)
      : mesh.points,
  );
  if (!feature && Math.hypot(selected.x - p.x, selected.y - p.y) > 25) return;
  event.preventDefault();
  stopRecovery();
  const handle = handles.find((h) => h.dataset.handle === String(selected.id));
  handle.focus({ preventScroll: true });
  active = {
    id: selected.id,
    pointer: event.pointerId,
    origin: p,
    start: mesh.snapshot(),
    weights: mesh.influence(selected.id),
    moved: false,
  };
  svg.setPointerCapture(event.pointerId);
});
svg.addEventListener("pointermove", (event) => {
  if (!active || event.pointerId !== active.pointer) return;
  const p = point(event),
    dx = p.x - active.origin.x,
    dy = p.y - active.origin.y;
  active.moved ||= Math.hypot(dx, dy) > 2;
  mesh.deform(active.start, active.weights, dx, dy);
  draw();
});
function release(event) {
  if (!active || event.pointerId !== active.pointer) return;
  const finished = active;
  active = null;
  if (svg.hasPointerCapture(finished.pointer))
    svg.releasePointerCapture(finished.pointer);
  if (finished.moved) {
    remember(finished.id);
    beginRecovery();
    status.textContent =
      "The template pulls the face back. A circle marks your displaced node.";
  }
}
svg.addEventListener("pointerup", release);
svg.addEventListener("pointercancel", release);
svg.addEventListener("lostpointercapture", release);
svg.addEventListener("keydown", (event) => {
  const directions = {
    ArrowLeft: [-1, 0],
    ArrowRight: [1, 0],
    ArrowUp: [0, -1],
    ArrowDown: [0, 1],
  };
  if (!directions[event.key]) return;
  const handle = event.target.closest("[data-handle]"),
    feature = event.target.closest("[data-feature]");
  if (!handle && !feature) return;
  event.preventDefault();
  stopRecovery();
  const id =
    handle?.dataset.handle ?? config.attachments[feature.dataset.feature][0];
  const [dx, dy] = directions[event.key],
    step = event.shiftKey ? 40 : 12;
  mesh.deform(mesh.snapshot(), mesh.influence(id), dx * step, dy * step);
  draw();
  keyTimer = setTimeout(() => {
    remember(id);
    beginRecovery();
  }, 650);
  status.textContent =
    "Node moved. Connected regions follow; the template will pull back.";
});
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  const pointer = active?.pointer;
  active = null;
  if (pointer !== undefined && svg.hasPointerCapture(pointer))
    svg.releasePointerCapture(pointer);
  stopRecovery();
  mesh.reset();
  history.splice(0);
  traces.replaceChildren();
  draw();
  status.textContent = "Face and gesture traces reset.";
});
draw();
