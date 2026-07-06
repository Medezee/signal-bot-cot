import xml.etree.ElementTree as ET
from datetime import datetime

from core.models import CursorOnTarget


def cot_time(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def transform_cot_to_xml(cot: CursorOnTarget) -> bytes:
    root = ET.Element("event")
    root.set("version", "2.0")
    root.set("type", cot.type.replace(".", cot.affiliation))  
    root.set("uid", str(cot.uid))
    root.set("how", cot.how)
    root.set("time", cot_time(cot.time))
    root.set("start", cot_time(cot.start))
    root.set("stale", cot_time(cot.stale))  

    ET.SubElement(
        root,
        "point",
        attrib={
            "lat": str(cot.coords.latitude),
            "lon": str(cot.coords.longitude),
            "hae": "0",
            "ce": "10",
            "le": "10",
        },
    )

    detail = ET.SubElement(root, "detail")
    ET.SubElement(detail, "contact", attrib={"callsign": cot.description})

    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
