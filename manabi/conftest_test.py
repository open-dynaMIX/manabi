from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .token import Token


def make_req(config: Dict[str, Any], override_path: Optional[str] = None) -> str:
    t = Token.from_config(config)
    path = "asdf.docx"
    if override_path:
        path = override_path
    ti = t.make(path)
    return f"http://localhost:8080/dav/{ti.as_url()}"


def test_server_failure(server, config: Dict[str, Any]):
    res = requests.get(make_req(config, "blabla.pdf"))
    assert res.status_code == 404


def test_server_file(config: Dict[str, Any], server, server_dir: Path):
    with open(Path(server_dir, "asdf.docx"), "rb") as f:
        exp = f.read()
        res = requests.get(make_req(config))
        assert exp == res.content
