"""
GreenOps Transcend Duo — FastAPI Backend & 9-Tool MCP Server
Serves the 9-Stage Post-Code DevSecOps evaluator, ISO/IEC 21031 SCI calculator,
Google Cloud Run CFE% region router, Flow Registry v1 validator, and static workbench.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .transcend_engine import GreenOpsTranscendEngine, DEVSECOPS_STAGES, GCP_REGIONS, PRESET_WORKLOADS
from .mcp_server import handle_mcp_request, MCP_TOOLS

ROOT_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = ROOT_DIR / "public"

app = FastAPI(
    title="GreenOps Transcend Duo — 9-Stage Post-Code Autonomous DevSecOps & GreenOps Agent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = GreenOpsTranscendEngine(ROOT_DIR)


class EvaluateRequest(BaseModel):
    workload_id: str = "workload-clocked-omniguard-byo"
    target_region: Optional[str] = None


@app.get("/api/health")
def get_health() -> Dict[str, Any]:
    spec = engine.validate_duo_flow_specs()
    return {
        "status": "ok",
        "service": "GreenOps Transcend Duo",
        "stages_covered": 9,
        "duo_flow_schema_status": spec["status"],
        "mcp_tools_count": len(MCP_TOOLS),
        "google_cloud_target_region": "europe-north1 (94% CFE)",
    }


@app.get("/api/metadata")
def get_metadata() -> Dict[str, Any]:
    return {
        "stages": DEVSECOPS_STAGES,
        "gcp_regions": GCP_REGIONS,
        "workloads": PRESET_WORKLOADS,
        "flow_validation": engine.validate_duo_flow_specs(),
    }


@app.post("/api/evaluate")
def run_evaluation(req: EvaluateRequest) -> Dict[str, Any]:
    return engine.evaluate_workload(req.workload_id, req.target_region)


@app.post("/api/mcp")
def run_mcp(payload: Dict[str, Any]) -> Dict[str, Any]:
    return handle_mcp_request(payload, engine)


if PUBLIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="public")
