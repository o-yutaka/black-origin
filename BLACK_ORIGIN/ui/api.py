from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from BLACK_ORIGIN.kernel.runtime import build_runtime

app = FastAPI(title="BLACK ORIGIN Control Interface")
runtime = build_runtime()
last_context: dict[str, object] = {"message": "System booted"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run-cycle")
def run_cycle() -> dict[str, object]:
    global last_context
    last_context = runtime.run_cycle()
    return {"cycle": last_context["cycle"], "status": "completed"}


@app.get("/status")
def status() -> dict[str, object]:
    loop = runtime.loop
    current_stage = loop.state.stage
    active_engines = [key for key in last_context.keys() if key not in {"cycle"}]
    tasks = last_context.get("agent_swarm_execution", {}).get("tasks", []) if isinstance(last_context, dict) else []
    return {
        "cycle": loop.state.cycle,
        "current_stage": current_stage,
        "active_engines": active_engines,
        "tasks": tasks,
        "thinking": f"AI is thinking... {current_stage}",
        "progress": {
            "Dataset Discovery": 100 if "dataset_discovery" in last_context else 0,
            "Graph Update": 100 if "knowledge_graph_update" in last_context else 0,
            "Simulation Progress": 100 if "planetary_simulation" in last_context else 0,
        },
        "system_monitor": last_context.get("system_evolution", {}).get("observability", {}),
    }


@app.get("/ui", response_class=HTMLResponse)
def ui() -> str:
    return """
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>BLACK ORIGIN</title>
  <script src='https://cdn.jsdelivr.net/npm/three@0.167.1/build/three.min.js'></script>
  <style>
    body { margin:0; font-family: Inter, Arial; background:#0b0f1f; color:#dce3ff; display:flex; height:100vh; }
    .sidebar { width:240px; background:#131a33; padding:16px; }
    .sidebar h3 { margin-top:0; }
    .main { flex:1; display:flex; flex-direction:column; }
    .top { padding:12px; background:#10162b; display:flex; gap:20px; }
    .grid { display:grid; grid-template-columns: 1fr 1fr; gap:12px; padding:12px; flex:1; }
    .panel { background:#141d3a; border-radius:10px; padding:12px; }
    #globe { height:260px; }
    .thinking { color:#7fbeff; font-style:italic; }
    button { background:#3478f6; color:white; border:none; padding:8px 12px; border-radius:8px; cursor:pointer; }
    .circles { display:flex; gap:12px; }
    .circle { width:84px; height:84px; border-radius:50%; border:8px solid #2b3357; display:flex; align-items:center; justify-content:center; }
  </style>
</head>
<body>
  <div class='sidebar'>
    <h3>BLACK ORIGIN</h3>
    <div>Chat</div><div>Agents</div><div>Tasks</div><div>World Graph</div><div>Memory</div><div>Data Streams</div><div>Simulation</div><div>Planetary Data Index</div><div>Nodes</div><div>Logs</div><div>System</div><div>Settings</div>
  </div>
  <div class='main'>
    <div class='top'>
      <div>System Status: <span id='status'>booting</span></div>
      <div>Cluster Nodes: <span id='nodes'>-</span></div>
      <div>Data Streams: Kafka</div>
      <div>Active Engine: <span id='engine'>-</span></div>
      <button onclick='runCycle()'>Run Cycle</button>
    </div>
    <div class='grid'>
      <div class='panel'>
        <h4>Control Chat</h4>
        <div class='thinking' id='thinking'>AI is thinking...</div>
        <pre id='tasks'></pre>
      </div>
      <div class='panel'>
        <h4>AI Process Progress</h4>
        <div class='circles'>
          <div class='circle' id='p1'>0%</div>
          <div class='circle' id='p2'>0%</div>
          <div class='circle' id='p3'>0%</div>
        </div>
      </div>
      <div class='panel'>
        <h4>3D Planetary Graph</h4>
        <div id='globe'></div>
      </div>
      <div class='panel'>
        <h4>System Monitor</h4>
        <pre id='monitor'></pre>
      </div>
    </div>
  </div>
<script>
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 2, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
const globeEl = document.getElementById('globe');
renderer.setSize(globeEl.clientWidth, globeEl.clientHeight);
globeEl.appendChild(renderer.domElement);
const geo = new THREE.SphereGeometry(1, 32, 32);
const mat = new THREE.MeshBasicMaterial({ color: 0x2d88ff, wireframe: true });
const sphere = new THREE.Mesh(geo, mat);
scene.add(sphere); camera.position.z = 2.2;
function animate() { requestAnimationFrame(animate); sphere.rotation.y += 0.01; renderer.render(scene, camera); }
animate();

async function runCycle(){ await fetch('/run-cycle', {method:'POST'}); await refresh(); }
async function refresh(){
  const r = await fetch('/status'); const s = await r.json();
  document.getElementById('status').innerText = 'online';
  document.getElementById('nodes').innerText = s.system_monitor.cluster_nodes || '-';
  document.getElementById('engine').innerText = s.current_stage;
  document.getElementById('thinking').innerText = s.thinking;
  document.getElementById('tasks').innerText = JSON.stringify(s.tasks, null, 2);
  const vals = Object.values(s.progress);
  document.getElementById('p1').innerText = vals[0] + '%';
  document.getElementById('p2').innerText = vals[1] + '%';
  document.getElementById('p3').innerText = vals[2] + '%';
  document.getElementById('monitor').innerText = JSON.stringify(s.system_monitor, null, 2);
}
refresh();
setInterval(refresh, 4000);
</script>
</body></html>
"""
