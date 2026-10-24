import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.transcend_engine import (
    DEVSECOPS_STAGES,
    GCP_REGIONS,
    PRESET_WORKLOADS,
    GreenOpsTranscendEngine,
    compute_sci_score,
)
from backend.mcp_server import handle_mcp_request, MCP_TOOLS


def test_official_9_gitlab_stages_covered():
    assert len(DEVSECOPS_STAGES) == 9
    assert [s["id"] for s in DEVSECOPS_STAGES] == [
        "plan",
        "create",
        "verify",
        "package",
        "secure",
        "release",
        "configure",
        "monitor",
        "govern",
    ]
    engine = GreenOpsTranscendEngine(ROOT_DIR)
    report = engine.evaluate_workload("workload-clocked-omniguard-byo")
    assert report["stages_covered_count"] == 9
    assert len(report["stages"]) == 9
    assert all(s["status"] == "passed" for s in report["stages"])


def test_iso_21031_sci_reduction_and_google_cloud_routing():
    engine = GreenOpsTranscendEngine(ROOT_DIR)
    report = engine.evaluate_workload("workload-clocked-omniguard-byo", "europe-north1")
    assert report["sci_reduction_percent"] > 90.0
    assert report["annual_kg_co2_saved"] > 15000.0
    assert report["target_region"]["region"] == "europe-north1"
    assert report["target_region"]["cfe_percent"] == 94.0

    sci = compute_sci_score(0.19, 42.0, 1.6)
    assert sci["sci_gco2eq_per_1k_requests"] < 12.0


def test_official_gitlab_duo_flow_v1_schema_validation():
    engine = GreenOpsTranscendEngine(ROOT_DIR)
    v = engine.validate_duo_flow_specs()
    assert v["status"] == "valid"
    assert v["passed_count"] == v["total_checks"] == 6


def test_mcp_jsonrpc_server_tools():
    assert len(PRESET_WORKLOADS) == 3
    assert len(MCP_TOOLS) == 9
    engine = GreenOpsTranscendEngine(ROOT_DIR)

    list_resp = handle_mcp_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, engine)
    assert len(list_resp["result"]["tools"]) == 9

    call_resp = handle_mcp_request(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "gitlab_duo_stage_configure",
                "arguments": {
                    "workload_id": "workload-clocked-omniguard-byo",
                    "target_region": "europe-north1",
                },
            },
        },
        engine,
    )
    assert call_resp["result"]["status"] == "passed"
    assert call_resp["result"]["target_gcp_region"] == "europe-north1"
