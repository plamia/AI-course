import pytest
import subprocess
import csv
import os
import sys
from pathlib import Path

@pytest.fixture
def run_cli(tmp_path):
    """Helper fixture to run the logsum CLI module using sys.executable."""
    def _run(input_content, args=None):
        if args is None:
            args = []
        input_file = tmp_path / "events.csv"
        input_file.write_text(input_content, encoding="utf-8")
        
        output_file = tmp_path / "summary.csv"
        
        cmd = [sys.executable, "-m", "src.logsum", "--input", str(input_file), "--output", str(output_file)] + args
        
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        return result, output_file
    return _run

def test_basic_grouping_and_normalisation(run_cli):
    """Test standard service/level normalisation and counting."""
    csv_data = (
        "timestamp,level,service,message\n"
        "2024-01-15T13:45:30Z, INFO , Auth-Service , login\n"
        "2024-01-15T13:46:00Z,info,auth-service,refresh\n"
    )
    result, out_file = run_cli(csv_data)
    assert result.returncode == 0
    
    with open(out_file, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    assert len(reader) == 1
    assert reader[0]["service"] == "auth-service"
    assert reader[0]["level"] == "INFO"
    assert reader[0]["count"] == "2"
    assert reader[0]["first_seen"] == "2024-01-15T13:45:30Z"
    assert reader[0]["last_seen"] == "2024-01-15T13:46:00Z"

def test_missing_level_edge_case(run_cli):
    """Test that missing levels are normalised to 'UNKNOWN' and counted."""
    csv_data = (
        "timestamp,level,service,message\n"
        "2024-01-15T13:45:30Z,, auth-service , missing level event\n"
    )
    result, out_file = run_cli(csv_data)
    assert result.returncode == 0
    
    with open(out_file, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    assert len(reader) == 1
    assert reader[0]["level"] == "UNKNOWN"
    assert reader[0]["count"] == "1"

def test_malformed_timestamp_edge_case(run_cli):
    """Test that malformed timestamps are counted but excluded from bounds."""
    csv_data = (
        "timestamp,level,service,message\n"
        "not-a-timestamp,WARN,payment-api,bad ts\n"
    )
    result, out_file = run_cli(csv_data)
    assert result.returncode == 0
    
    with open(out_file, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    assert len(reader) == 1
    assert reader[0]["count"] == "1"
    assert reader[0]["first_seen"] == ""
    assert reader[0]["last_seen"] == ""

def test_empty_input_header_only(run_cli):
    """Test empty input (header only) produces header-only summary and exit 0."""
    csv_data = "timestamp,level,service,message\n"
    result, out_file = run_cli(csv_data)
    assert result.returncode == 0
    
    with open(out_file, encoding="utf-8") as f:
        content = f.read().strip()
    
    assert content == "service,level,count,first_seen,last_seen"

def test_missing_input_file_error(tmp_path):
    """Test missing input file exits with code 2."""
    output_file = tmp_path / "summary.csv"
    non_existent = tmp_path / "does_not_exist.csv"
    
    cmd = [sys.executable, "-m", "src.logsum", "--input", str(non_existent), "--output", str(output_file)]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 2

def test_output_default_argument(tmp_path):
    """Test default output path behavior when --output is omitted."""
    input_file = tmp_path / "events.csv"
    input_file.write_text("timestamp,level,service,message\n2024-01-15T13:45:30Z,INFO,api,test\n", encoding="utf-8")
    
    cmd = [sys.executable, "-m", "src.logsum", "--input", str(input_file)]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()
    
    result = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert (tmp_path / "summary.csv").exists()

def test_multiple_distinct_groups(run_cli):
    """Test multiple distinct service/level groups are sorted and separated."""
    csv_data = (
        "timestamp,level,service,message\n"
        "2024-01-15T13:00:00Z,ERROR,auth,fail\n"
        "2024-01-15T13:00:00Z,INFO,billing,ok\n"
    )
    result, out_file = run_cli(csv_data)
    assert result.returncode == 0
    
    with open(out_file, encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
    
    assert len(reader) == 2
    assert reader[0]["service"] == "auth" and reader[0]["level"] == "ERROR"
    assert reader[1]["service"] == "billing" and reader[1]["level"] == "INFO"