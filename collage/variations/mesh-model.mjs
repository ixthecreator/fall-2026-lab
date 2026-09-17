// Artistic deformation rules. This does not run face recognition.
export function createMesh(nodes, edges) {
  const points = nodes.map((n) => ({ ...n, homeX: n.x, homeY: n.y }));
  const byId = new Map(points.map((n, i) => [String(n.id), i]));
  const adjacency = points.map(() => []);
  const links = edges.map(({ a, b }) => {
    const i = byId.get(String(a)),
      j = byId.get(String(b));
    const length = Math.hypot(
      points[i].x - points[j].x,
      points[i].y - points[j].y,
    );
    adjacency[i].push([j, length]);
    adjacency[j].push([i, length]);
    return { i, j, length };
  });
  function influence(id) {
    // Distance travels along the actual mesh edges, not across a flat radius.
    const distance = points.map(() => Infinity),
      visited = new Set();
    distance[byId.get(String(id))] = 0;
    while (visited.size < points.length) {
      let next = -1;
      for (let i = 0; i < points.length; i++)
        if (!visited.has(i) && (next < 0 || distance[i] < distance[next]))
          next = i;
      if (next < 0 || !Number.isFinite(distance[next])) break;
      visited.add(next);
      for (const [j, length] of adjacency[next])
        distance[j] = Math.min(distance[j], distance[next] + length);
    }
    return distance.map((d) => Math.exp(-d / 115));
  }
  function snapshot() {
    return points.map(({ x, y }) => ({ x, y }));
  }
  function deform(start, weights, dx, dy) {
    points.forEach((n, i) => {
      n.x = Math.max(24, Math.min(976, start[i].x + weights[i] * dx));
      n.y = Math.max(24, Math.min(1076, start[i].y + weights[i] * dy));
    });
  }
  function restore(start, retained) {
    points.forEach((n, i) => {
      n.x = n.homeX + (start[i].x - n.homeX) * retained;
      n.y = n.homeY + (start[i].y - n.homeY) * retained;
    });
  }
  function reset() {
    points.forEach((n) => {
      n.x = n.homeX;
      n.y = n.homeY;
    });
  }
  return { points, byId, links, influence, snapshot, deform, restore, reset };
}
