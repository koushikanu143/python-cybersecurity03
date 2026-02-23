import xml.etree.ElementTree as ET

report_file = r"C:\PeStudioReports\sample.xml"

tree = ET.parse(report_file)
root = tree.getroot()

for indicator in root.findall(".//indicator"):
    name = indicator.get("name")
    severity = indicator.get("severity")
    print(f"{name} → Severity: {severity}")