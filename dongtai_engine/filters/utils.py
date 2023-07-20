from http.client import parse_headers
from io import BytesIO
from tempfile import SpooledTemporaryFile, TemporaryFile

# Request{method=GET, url=http://www.baidu.com/, tag=null}


class JavaObjects:
    def __init__(self, objects_classname, objects_attrs):
        self.objects_classname = objects_classname
        self.objects_attrs = objects_attrs
        for name, value in objects_attrs:
            setattr(self, name, value)

    def __str__(self):
        attrs_string = ", ".join(
            [f"{name}={value}" for name, value in self.objects_attrs]
        )
        return f"{self.objects_classname}{{{attrs_string}}}"


def parse_java_objects(objects_string: str):
    objects_classname = objects_string[: objects_string.index("{")]
    objects_attrstring = objects_string[objects_string.index("{") :]
    objects_attrs = [
        attr.split("=", 2) for attr in objects_attrstring.strip("{}").split(", ")
    ]
    return JavaObjects(objects_classname, objects_attrs)


def parse_headers_dict_from_bytes(header_bytes: bytes) -> dict:
    with SpooledTemporaryFile(max_size=10000) as fp:
        fp.write(header_bytes)
        fp.seek(0)
        return dict(parse_headers(fp))  # type:ignore
