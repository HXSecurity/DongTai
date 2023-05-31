from typing import List
from typing import Any
from typing import Optional
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime


@dataclass_json
@dataclass
class Reference:
    type: str = ""
    url: str = ""


@dataclass_json
@dataclass
class VulCodes:
    CVE: List[str] = []
    GHSA: List[str] = []


@dataclass_json
@dataclass
class VulInfo:
    vul_id: str = ""
    cvss_v3: str = ""
    cwe: List[str] = []
    title: str = ""
    description: str = ""
    references: List[Reference] = []
    severity: str = []
    published_time: Optional[datetime] = field(
        default=None,
        metadata=config(decoder=lambda x: datetime.fromisoformat(x)
                        if x is not None else None,
                        encoder=lambda x: datetime.isoformat(x)
                        if x is not None else None))
    create_time: datetime = field(default=datetime.now(),
                                  metadata=config(
                                      decoder=datetime.fromisoformat,
                                      encoder=datetime.isoformat))
    update_time: datetime = field(default=datetime.now(),
                                  metadata=config(
                                      decoder=datetime.fromisoformat,
                                      encoder=datetime.isoformat))
    change_time: datetime = field(default=datetime.now(),
                                  metadata=config(
                                      decoder=datetime.fromisoformat,
                                      encoder=datetime.isoformat))


@dataclass_json
@dataclass
class Vul:
    vul_info: VulInfo
    vul_codes: VulCodes
    affected_versions: List[str] = []


@dataclass_json
@dataclass
class Data:
    vuls: List[Vul] = []
    affected_versions: List[str] = []
    unaffected_versions: List[str] = []


@dataclass_json
@dataclass
class PackageInfo:
    ecosystem: str
    language: str
    name: str
    version: str
    hash: str
    license: List[str]
    version_publish_time: str

@dataclass_json
@dataclass
class Root:
    status: int
    msg: str
    data: Data
