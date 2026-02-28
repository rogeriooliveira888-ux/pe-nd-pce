from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = PROJECT_ROOT / "reports_output"

def create_chart(dcf):
    chart_path = OUTPUT_PATH / "dcf_chart.png"
    plt.figure()
    plt.bar(["Pessimista","Base","Otimista"],
            [dcf["Pessimista"], dcf["Base"], dcf["Otimista"]])
    plt.title("DCF Cenários")
    plt.savefig(chart_path)
    plt.close()
    return chart_path

def generate_report(data, filename="investment_report.pdf"):
    OUTPUT_PATH.mkdir(exist_ok=True)
    file_path = OUTPUT_PATH / filename

    chart = create_chart(data["DCF"])

    doc = SimpleDocTemplate(str(file_path))
    styles = getSampleStyleSheet()

    story = [
        Paragraph("PE-ND-PCE Investment Report", styles["Title"]),
        Spacer(1,20),
        Paragraph("Valuation", styles["Heading2"]),
        Paragraph(str(data["DCF"]), styles["Normal"]),
        Spacer(1,20),
        Image(str(chart), width=400, height=200),
        Spacer(1,20),
        Paragraph("Decision", styles["Heading2"]),
        Paragraph(str(data["Decision"]), styles["Normal"]),
    ]

    doc.build(story)
    print("Relatório salvo em:", file_path)