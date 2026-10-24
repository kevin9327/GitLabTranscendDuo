"""
GreenOps Transcend Duo — 9-Tool Model Context Protocol (MCP) JSON-RPC 2.0 Server
Exposes 1 tool per GitLab DevSecOps stage (`plan` .. `govern`) to GitLab Duo Agents & IDEs.
"""

from __future__ import annotations

from typing import Any, Dict, List
from .transcend_engine import GreenOpsTranscendEngine, DEVSECOPS_STAGES


MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": f"gitlab_duo_stage_{s['id']}",
        "stage_index": s["index"],
        "stage_id": s["id"],
        "description": f"Stage {s['index']} ({s['title']}): {s['focus']}",
        "inputSchema": {
            "type": "object",
            "properties": {
                "workload_id": {"type": "string", "default": "workload-clocked-omniguard-byo"},
                "target_region": {"type": "string", "default": "europe-north1"},
            },
        },
    }
    for s in DEVSECOPS_STAGES
]


def handle_mcp_request(payload: Dict[str, Any], engine: GreenOpsTranscendEngine) -> Dict[str, Any]:
    req_id = payload.get("id", 1)
    method = payload.get("method", "tools/list")
    params = payload.get("params") or {}

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "server": "greenops-transcend-duo-mcp",
                "version": "1.0.0",
                "stages_covered": 9,
                "tools": MCP_TOOLS,
            },
        }

    if method == "tools/call":
        name = params.get("name", "gitlab_duo_stage_plan")
        args = params.get("arguments") or {}
        wl_id = args.get("workload_id", "workload-clocked-omniguard-byo")
        tgt_reg = args.get("target_region")

        report = engine.evaluate_workload(wl_id, tgt_reg)
        stg_id = name.replace("gitlab_duo_stage_", "")
        stg_out = next((s for s in report["stages"] if s["stage_id"] == stg_id), report["stages"][0])

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tool": name,
                "stage_id": stg_out["stage_id"],
                "status": stg_out["status"],
                "sci_reduction_percent": report["sci_reduction_percent"],
                "target_gcp_region": report["target_region"]["region"],
                "target_gcp_cfe_percent": report["target_region"]["cfe_percent"],
                "stage_output": stg_out,
                "attestation_sha256": report["attestation_sha256"],
            },
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Unsupported MCP method: {method}"},
    }
