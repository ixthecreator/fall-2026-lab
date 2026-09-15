// HTML and Grid set the composition. JavaScript only moves its seven fragments.
const stage = document.querySelector(".stage");
const fragments = [...stage.querySelectorAll(".fragment")];
const drawing = stage.querySelector(".connections");
const status = document.querySelector(".status");
const ns = "http://www.w3.org/2000/svg";
const positions = fragments.map(() => ({ x: 0, y: 0 }));
const edges = [
  [0, 1],
  [0, 2],
  [1, 2],
  [2, 3],
  [0, 4],
  [3, 5],
  [1, 6],
  [4, 5],
  [5, 6],
];
let active = null;
let topLayer = 4;

function point(element) {
  const rect = element.getBoundingClientRect();
  const area = stage.getBoundingClientRect();
  return {
    x: rect.left + rect.width / 2 - area.left,
    y: rect.top + rect.height / 2 - area.top,
  };
}

function mark(tag, attributes) {
  const element = document.createElementNS(ns, tag);
  for (const [name, value] of Object.entries(attributes))
    element.setAttribute(name, value);
  drawing.append(element);
}

function drawConnections() {
  const width = stage.clientWidth;
  const height = stage.clientHeight;
  drawing.setAttribute("viewBox", `0 0 ${width} ${height}`);
  drawing.replaceChildren();
  const points = fragments.map((fragment) =>
    point(fragment.querySelector(".handle")),
  );
  for (const [a, b] of edges)
    mark("line", {
      x1: points[a].x,
      y1: points[a].y,
      x2: points[b].x,
      y2: points[b].y,
    });
  // Fixed peripheral points make the photographic face and moving pieces share a map.
  const anchors = [
    [0.4, 0.25],
    [0.73, 0.24],
    [0.28, 0.52],
    [0.83, 0.57],
    [0.53, 0.86],
  ];
  anchors.forEach(([x, y], i) => {
    const target = points[i % points.length];
    mark("line", { x1: x * width, y1: y * height, x2: target.x, y2: target.y });
    mark("circle", { cx: x * width, cy: y * height, r: 5, class: "anchor" });
  });
  points.forEach(({ x, y }) => mark("circle", { cx: x, cy: y, r: 4 }));
}

function move(index, x, y) {
  const fragment = fragments[index];
  const area = stage.getBoundingClientRect();
  const rect = fragment.getBoundingClientRect();
  const baseX = rect.left - area.left - positions[index].x * area.width;
  const baseY = rect.top - area.top - positions[index].y * area.height;
  // Keep the entire rotated fragment within its stage, including its border.
  const px = Math.min(
    Math.max(x * area.width, -baseX),
    area.width - baseX - rect.width,
  );
  const py = Math.min(
    Math.max(y * area.height, -baseY),
    area.height - baseY - rect.height,
  );
  positions[index] = { x: px / area.width, y: py / area.height };
  fragment.style.setProperty("--dx", `${px}px`);
  fragment.style.setProperty("--dy", `${py}px`);
  drawConnections();
}

function announce(index) {
  status.textContent = `${fragments[index].querySelector("button").getAttribute("aria-label").replace("Move ", "")} moved. A different face, already.`;
}

fragments.forEach((fragment, index) => {
  const handle = fragment.querySelector("button");
  handle.addEventListener("pointerdown", (event) => {
    if (event.button !== 0 || active) return;
    handle.focus({ preventScroll: true });
    fragment.style.zIndex = ++topLayer;
    active = {
      index,
      pointer: event.pointerId,
      startX: event.clientX,
      startY: event.clientY,
      ...positions[index],
    };
    handle.setPointerCapture(event.pointerId);
  });
  handle.addEventListener("pointermove", (event) => {
    if (!active || active.pointer !== event.pointerId || active.index !== index)
      return;
    move(
      index,
      active.x + (event.clientX - active.startX) / stage.clientWidth,
      active.y + (event.clientY - active.startY) / stage.clientHeight,
    );
  });
  const endDrag = (event) => {
    if (!active || active.pointer !== event.pointerId) return;
    active = null;
    announce(index);
  };
  handle.addEventListener("pointerup", endDrag);
  handle.addEventListener("pointercancel", endDrag);
  handle.addEventListener("lostpointercapture", endDrag);
  handle.addEventListener("keydown", (event) => {
    const direction = {
      ArrowLeft: [-1, 0],
      ArrowRight: [1, 0],
      ArrowUp: [0, -1],
      ArrowDown: [0, 1],
    }[event.key];
    if (!direction) return;
    event.preventDefault();
    fragment.style.zIndex = ++topLayer;
    const step = event.shiftKey ? 24 : 8;
    move(
      index,
      positions[index].x + (direction[0] * step) / stage.clientWidth,
      positions[index].y + (direction[1] * step) / stage.clientHeight,
    );
    announce(index);
  });
});

new ResizeObserver(() => {
  fragments.forEach((fragment, index) => {
    fragment.style.setProperty(
      "--dx",
      `${positions[index].x * stage.clientWidth}px`,
    );
    fragment.style.setProperty(
      "--dy",
      `${positions[index].y * stage.clientHeight}px`,
    );
  });
  drawConnections();
}).observe(stage);
drawConnections();
