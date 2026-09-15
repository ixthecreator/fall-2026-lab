const network = {
  nodes: [
    { id: "n01", x: 243, y: 354 },
    { id: "n02", x: 323, y: 366 },
    { id: "n03", x: 374, y: 370 },
    { id: "n04", x: 417, y: 375 },
    { id: "n05", x: 484, y: 360 },
    { id: "n06", x: 543, y: 345 },
    { id: "n07", x: 213, y: 420 },
    { id: "n08", x: 337, y: 395 },
    { id: "n09", x: 373, y: 419 },
    { id: "n10", x: 515, y: 433 },
    { id: "n11", x: 229, y: 504 },
    { id: "n12", x: 347, y: 464 },
    { id: "n13", x: 530, y: 477 },
    { id: "n14", x: 330, y: 505 },
    { id: "n15", x: 407, y: 507 },
    { id: "n16", x: 276, y: 548 },
    { id: "n17", x: 368, y: 553 },
    { id: "n18", x: 484, y: 551 },
    { id: "n19", x: 345, y: 623 },
    { id: "n20", x: 387, y: 627 },
    { id: "n21", x: 291, y: 657 },
    { id: "n22", x: 459, y: 670 },
  ],
  edges: [
    { a: "n01", b: "n02", color: "#29252b" },
    { a: "n01", b: "n07", color: "#29252b" },
    { a: "n01", b: "n08", color: "#29252b" },
    { a: "n02", b: "n03", color: "#ff940a" },
    { a: "n02", b: "n08", color: "#91476d" },
    { a: "n03", b: "n04", color: "#ff940a" },
    { a: "n03", b: "n08", color: "#ff940a" },
    { a: "n03", b: "n09", color: "#ff940a" },
    { a: "n04", b: "n05", color: "#ff940a" },
    { a: "n04", b: "n09", color: "#ff940a" },
    { a: "n04", b: "n10", color: "#ff940a" },
    { a: "n05", b: "n06", color: "#ff940a" },
    { a: "n05", b: "n10", color: "#ff940a" },
    { a: "n06", b: "n10", color: "#ff940a" },
    { a: "n07", b: "n08", color: "#29252b" },
    { a: "n07", b: "n11", color: "#29252b" },
    { a: "n08", b: "n09", color: "#ff940a" },
    { a: "n08", b: "n12", color: "#29252b" },
    { a: "n09", b: "n12", color: "#29252b" },
    { a: "n09", b: "n15", color: "#ff940a" },
    { a: "n10", b: "n13", color: "#ff940a" },
    { a: "n10", b: "n15", color: "#ff940a" },
    { a: "n11", b: "n12", color: "#29252b" },
    { a: "n11", b: "n14", color: "#29252b" },
    { a: "n11", b: "n16", color: "#29252b" },
    { a: "n12", b: "n14", color: "#29252b" },
    { a: "n13", b: "n18", color: "#ff940a" },
    { a: "n14", b: "n16", color: "#29252b" },
    { a: "n14", b: "n17", color: "#29252b" },
    { a: "n15", b: "n17", color: "#ff940a" },
    { a: "n15", b: "n18", color: "#ff940a" },
    { a: "n16", b: "n21", color: "#29252b" },
    { a: "n16", b: "n19", color: "#29252b" },
    { a: "n17", b: "n19", color: "#29252b" },
    { a: "n17", b: "n20", color: "#ff940a" },
    { a: "n18", b: "n20", color: "#ff940a" },
    { a: "n18", b: "n22", color: "#ff940a" },
    { a: "n19", b: "n21", color: "#29252b" },
    { a: "n20", b: "n22", color: "#ff940a" },
  ],
};
const artwork = document.querySelector(".artwork");
const nodeLayer = artwork.querySelector(".nodes");
const connections = artwork.querySelector(".connections");
const status = document.querySelector(".status");
const ns = "http://www.w3.org/2000/svg";
const nodes = network.nodes.map((node) => ({
  ...node,
  kind: "node",
  homeX: node.x,
  homeY: node.y,
  element: artwork.querySelector(`[data-node="${node.id}"]`),
}));
const byId = new Map(nodes.map((node) => [node.id, node]));
const features = [...artwork.querySelectorAll(".feature")].map((element) => ({
  kind: "feature",
  element,
  id: element.dataset.feature,
  x: Number(element.getAttribute("x")),
  y: Number(element.getAttribute("y")),
  homeX: Number(element.getAttribute("x")),
  homeY: Number(element.getAttribute("y")),
  width: Number(element.getAttribute("width")),
  height: Number(element.getAttribute("height")),
  hole: artwork.querySelector(`[data-hole="${element.dataset.feature}"]`),
}));
const items = [...nodes, ...features];
const edges = network.edges.map((edge) => {
  const line = document.createElementNS(ns, "line");
  line.style.stroke = edge.color;
  line.dataset.edge = `${edge.a}-${edge.b}`;
  connections.append(line);
  return { ...edge, line };
});
// Facial patches carry nearby landmarks; every landmark can also move alone.
const attachments = {
  "left-eye": ["n07", "n08", "n12"],
  "right-eye": ["n04", "n05", "n10", "n13"],
  nose: ["n09", "n14", "n15", "n17"],
  mouth: ["n19", "n20", "n21", "n22"],
};
let active = null;
function draw() {
  for (const node of nodes)
    node.element.setAttribute("transform", `translate(${node.x} ${node.y})`);
  for (const item of features) {
    item.element.setAttribute("x", item.x);
    item.element.setAttribute("y", item.y);
    const occlusion = artwork.querySelector(`[data-occlude="${item.id}"]`);
    if (occlusion) {
      occlusion.setAttribute("x", item.x);
      occlusion.setAttribute("y", item.y);
    }
    item.hole.setAttribute(
      "opacity",
      Math.abs(item.x - item.homeX) + Math.abs(item.y - item.homeY) > 0.5
        ? "1"
        : "0",
    );
  }
  for (const edge of edges) {
    const a = byId.get(edge.a),
      b = byId.get(edge.b);
    for (const [name, value] of Object.entries({
      x1: a.x,
      y1: a.y,
      x2: b.x,
      y2: b.y,
    }))
      edge.line.setAttribute(name, value);
  }
}
function move(item, x, y) {
  const previous = { x: item.x, y: item.y };
  const margin = item.kind === "node" ? 15 : 0;
  item.x = Math.max(margin, Math.min(749 - (item.width ?? margin), x));
  item.y = Math.max(margin, Math.min(1000 - (item.height ?? margin), y));
  if (item.kind === "feature") {
    for (const id of attachments[item.id]) {
      const node = byId.get(id);
      node.x = Math.max(15, Math.min(734, node.x + item.x - previous.x));
      node.y = Math.max(15, Math.min(985, node.y + item.y - previous.y));
    }
  }
  draw();
}
function restore() {
  active = null;
  for (const item of items) {
    item.x = item.homeX;
    item.y = item.homeY;
  }
  draw();
  status.textContent = "All 22 nodes and facial features restored.";
}
function raise(item) {
  if (item.kind === "node") nodeLayer.append(item.element);
  else artwork.insertBefore(item.element, connections);
}
for (const item of items) {
  const element = item.element;
  element.addEventListener("pointerdown", (event) => {
    if (event.button !== 0 || active) return;
    event.preventDefault();
    element.focus({ preventScroll: true });
    raise(item);
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
  for (const event of ["pointerup", "pointercancel", "lostpointercapture"])
    element.addEventListener(event, release);
  element.addEventListener("keydown", (event) => {
    const d = {
      ArrowLeft: [-1, 0],
      ArrowRight: [1, 0],
      ArrowUp: [0, -1],
      ArrowDown: [0, 1],
    }[event.key];
    if (!d) return;
    event.preventDefault();
    raise(item);
    const step = event.shiftKey ? 20 : 3;
    move(item, item.x + d[0] * step, item.y + d[1] * step);
    status.textContent =
      element.getAttribute("aria-label").replace("Move ", "") + " moved.";
  });
}
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") restore();
});
draw();
