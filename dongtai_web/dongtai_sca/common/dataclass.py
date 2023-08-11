from dataclasses import dataclass, field
from datetime import datetime

from dataclasses_json import config, dataclass_json
from dateutil.parser import parse

# those Union[tuple[str], tuple[()]] = () is not working
# Since https://github.com/lidatong/dataclasses-json/pull/409
# Be careful with potentially nullable types when using them temporarily.


@dataclass_json
@dataclass
class I18nStr:
    en: str = ""
    zh: str = ""


@dataclass_json
@dataclass
class Reference:
    type: str = ""
    url: str = ""
    language: str = ""


@dataclass_json
@dataclass
class VulCodes:
    CVE: tuple[str, ...] = ()
    GHSA: tuple[str, ...] = ()


@dataclass_json
@dataclass
class VulInfo:
    vul_id: str = ""
    cvss_v3: str = ""
    cwe: tuple[str, ...] = ()
    title: I18nStr = field(default_factory=I18nStr)
    description: I18nStr = field(default_factory=I18nStr)
    references: tuple[Reference, ...] = ()
    severity: str = ""
    published_time: datetime | None = field(
        default=None,
        metadata=config(
            decoder=lambda x: parse(x) if x is not None else None,
            encoder=lambda x: datetime.isoformat(x) if x is not None else None,
        ),
    )
    create_time: datetime = field(
        default=datetime.now(),
        metadata=config(decoder=parse, encoder=datetime.isoformat),
    )
    update_time: datetime = field(
        default=datetime.now(),
        metadata=config(decoder=parse, encoder=datetime.isoformat),
    )
    change_time: datetime = field(
        default=datetime.now(),
        metadata=config(decoder=parse, encoder=datetime.isoformat),
    )


@dataclass_json
@dataclass
class Vul:
    vul_info: VulInfo
    vul_codes: VulCodes
    affected_versions: tuple[str, ...] = ()
    unaffected_versions: tuple[str, ...] = ()


@dataclass_json
@dataclass
class PackageVulData:
    vuls: tuple[Vul, ...] = ()
    affected_versions: tuple[str, ...] = ()
    unaffected_versions: tuple[str, ...] = ()


@dataclass_json
@dataclass
class PackageInfo:
    ecosystem: str
    language: str
    name: str
    version: str
    hash: str
    version_publish_time: str = ""
    license: tuple[str, ...] = ()


@dataclass_json
@dataclass
class PackageVulResponse:
    status: int
    msg: str
    data: PackageVulData


@dataclass_json
@dataclass
class PackageResponse:
    status: int
    msg: str
    data: tuple[PackageInfo, ...] = ()
