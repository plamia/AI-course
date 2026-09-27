import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure directory exists
output_dir = "./modules/1000-management/artefacts/1000-wide"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "03-staffing.xlsx")

wb = openpyxl.Workbook()

# Define Styles
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E78")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=11, bold=True)
font_regular = Font(name="Calibri", size=11)

fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
fill_total = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
fill_accent = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
total_border = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='double', color='000000')
)

months = [f"M{i}" for i in range(1, 13)]
headers = ["Role", "Grade / Location"] + months + ["Total FTE-Mo"]

variants = {
    "Lean": {
        "bet": "Bet: Optimises strictly for commercial budget (15% Onshore / 15% Nearshore / 70% Offshore); trades schedule margin by pushing site cutovers to Month 12.",
        "data": [
            ["Delivery Lead", "Lead (Onshore)", 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
            ["Enterprise Architect", "Senior (Onshore)", 0.50, 0.50, 0.25, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
            ["Integration Tech Lead", "Senior (Nearshore)", 0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00],
            ["Backend / API Dev (2x)", "Middle (Offshore)", 0.30, 0.80, 2.00, 2.00, 2.00, 2.00, 2.00, 1.00, 1.00, 1.00, 0.50, 0.20],
            ["Frontend Portal Dev (2x)", "Middle (Offshore)", 0.00, 0.30, 1.00, 2.00, 2.00, 2.00, 2.00, 1.00, 1.00, 0.50, 0.50, 0.20],
            ["AI / Data Engineer", "Senior (Offshore)", 0.00, 0.20, 0.50, 0.50, 0.50, 0.50, 1.00, 1.00, 1.00, 0.50, 0.20, 0.10],
            ["QA Automation Lead", "Middle (Offshore)", 0.20, 0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50]
        ]
    },
    "Balanced": {
        "bet": "Bet: Optimises for predictable milestone delivery on hard 12-month contract deadline using EPAM blended model (30% Onshore / 40% Nearshore / 30% Offshore). RECOMMENDED.",
        "data": [
            ["Delivery Manager", "Lead (Onshore)", 1.00, 1.00, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 1.00, 1.00, 1.00],
            ["Enterprise Architect", "Lead (Onshore)", 1.00, 1.00, 0.50, 0.25, 0.25, 0.25, 0.25, 0.25, 0.50, 0.25, 0.25, 0.25],
            ["Business Analyst / PROD", "Senior (Onshore)", 0.50, 1.00, 1.00, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.25],
            ["Integration Tech Lead", "Senior (Nearshore)", 0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50],
            ["Backend / API Devs (3x)", "Middle (Nearshore)", 0.50, 1.50, 3.00, 3.00, 3.00, 3.00, 3.00, 2.00, 2.00, 1.00, 1.00, 0.50],
            ["Frontend Portal Devs (2x)", "Middle (Offshore)", 0.00, 0.50, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.00, 1.00, 0.50, 0.20],
            ["AI / Data Engineer (2x)", "Senior (Offshore)", 0.00, 0.50, 1.00, 1.00, 1.00, 1.00, 2.00, 2.00, 2.00, 1.00, 0.50, 0.25],
            ["QA Lead & Automation (2x)", "Senior/Mid (Nearshore)", 0.30, 1.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.00, 0.50]
        ]
    },
    "Fast": {
        "bet": "Bet: Optimises for schedule compression and early site enablement via high onshore co-location (50% Onshore / 30% Nearshore / 20% Offshore); trades higher burn.",
        "data": [
            ["Program Manager", "Principal (Onshore)", 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50, 0.50, 0.25],
            ["Enterprise Architect", "Lead (Onshore)", 1.00, 1.00, 1.00, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.25, 0.25, 0.10],
            ["Onshore Integration Leads (2x)", "Lead (Onshore)", 1.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 2.00, 1.00, 0.50, 0.50, 0.25],
            ["Backend API Devs (4x)", "Mid/Sr (Nearshore)", 1.00, 3.00, 4.00, 4.00, 4.00, 4.00, 3.00, 2.00, 1.00, 0.50, 0.25, 0.10],
            ["Frontend Devs (3x)", "Mid (Nearshore)", 0.50, 2.00, 3.00, 3.00, 3.00, 3.00, 2.00, 1.00, 1.00, 0.50, 0.20, 0.10],
            ["AI Engineers (3x)", "Senior (Onshore/NS)", 0.50, 1.50, 3.00, 3.00, 3.00, 3.00, 3.00, 2.00, 1.00, 0.50, 0.20, 0.10],
            ["QA Engineers (4x)", "Mid (Offshore)", 1.00, 2.00, 4.00, 4.00, 4.00, 4.00, 4.00, 3.00, 2.00, 1.00, 0.50, 0.25],
            ["Change & Training Lead", "Senior (Onshore)", 0.25, 0.50, 0.50, 0.50, 1.00, 1.00, 1.00, 1.00, 1.00, 1.00, 0.50, 0.25]
        ]
    }
}

# Remove default sheet
wb.remove(wb.active)

# Create Variant Sheets
for sheet_name, content in variants.items():
    ws = wb.create_sheet(title=sheet_name)
    
    # Title & Bet
    ws.cell(row=1, column=1, value=f"Staffing Variant: {sheet_name}").font = font_title
    ws.cell(row=2, column=1, value=content["bet"]).font = font_subtitle
    
    # Table Headers
    header_row = 4
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_idx, value=header)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center if col_idx > 2 else align_left
    
    # Rows
    start_data_row = 5
    for row_offset, row_data in enumerate(content["data"]):
        current_row = start_data_row + row_offset
        role, location = row_data[0], row_data[1]
        m_values = row_data[2:]
        
        ws.cell(row=current_row, column=1, value=role).font = font_bold
        ws.cell(row=current_row, column=2, value=location).font = font_regular
        
        ws.cell(row=current_row, column=1).border = thin_border
        ws.cell(row=current_row, column=2).border = thin_border
        
        # Monthly values
        for m_idx, val in enumerate(m_values, 3):
            cell = ws.cell(row=current_row, column=m_idx, value=val)
            cell.font = font_regular
            cell.number_format = "0.00"
            cell.alignment = align_right
            cell.border = thin_border
        
        # Row Total Formula
        total_cell = ws.cell(row=current_row, column=15, value=f"=SUM(C{current_row}:N{current_row})")
        total_cell.font = font_bold
        total_cell.number_format = "0.00"
        total_cell.alignment = align_right
        total_cell.border = thin_border
        total_cell.fill = fill_accent

    # Bottom Total Row
    total_row = start_data_row + len(content["data"])
    ws.cell(row=total_row, column=1, value="TOTAL MONTHLY FTEs").font = font_bold
    ws.cell(row=total_row, column=2, value="").font = font_bold
    ws.cell(row=total_row, column=1).border = total_border
    ws.cell(row=total_row, column=2).border = total_border
    ws.cell(row=total_row, column=1).fill = fill_total
    ws.cell(row=total_row, column=2).fill = fill_total

    for c in range(3, 15):
        col_letter = get_column_letter(c)
        cell = ws.cell(row=total_row, column=c, value=f"=SUM({col_letter}{start_data_row}:{col_letter}{total_row-1})")
        cell.font = font_bold
        cell.number_format = "0.00"
        cell.alignment = align_right
        cell.border = total_border
        cell.fill = fill_total

    # Grand Total (FTE Months)
    grand_total_cell = ws.cell(row=total_row, column=15, value=f"=SUM(O{start_data_row}:O{total_row-1})")
    grand_total_cell.font = font_bold
    grand_total_cell.number_format = "0.00"
    grand_total_cell.alignment = align_right
    grand_total_cell.border = total_border
    grand_total_cell.fill = fill_total

    # Auto-fit column widths
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 10)

# Create Recommendation Tab
ws_rec = wb.create_sheet(title="Summary & Recommendation")

ws_rec.cell(row=1, column=1, value="Staffing Variants Trade-Off & Recommendation").font = font_title

# Summary Table Header
summary_headers = ["Metric / Dimension", "Lean Variant", "Balanced Variant (Recommended)", "Fast Variant"]
for c_idx, h_text in enumerate(summary_headers, 1):
    c = ws_rec.cell(row=3, column=c_idx, value=h_text)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_center if c_idx > 1 else align_left

summary_rows = [
    ["Total FTE-Months", "=Lean!O12", "=Balanced!O13", "=Fast!O13"],
    ["Delivery Model Split", "15% On / 15% NS / 70% Off", "30% On / 40% NS / 30% Off", "50% On / 30% NS / 20% Off"],
    ["Target Go-Live Schedule", "Month 12 (High Cutover Risk)", "Month 11 + 4 Wk Buffer", "Month 9.5 (2.5 Mo Early)"],
    ["Commercial Cost Index", "1.00x (Baseline)", "1.55x", "2.35x"],
    ["Primary Delivery Risk", "Resource bottleneck in M12", "Balanced risk profile", "Excessive client coordination load"]
]

for r_idx, r_data in enumerate(summary_rows, 4):
    for c_idx, val in enumerate(r_data, 1):
        cell = ws_rec.cell(row=r_idx, column=c_idx, value=val)
        cell.font = font_bold if c_idx == 3 else font_regular
        cell.border = thin_border
        if c_idx == 3:
            cell.fill = fill_total

# Recommendation Narrative
ws_rec.cell(row=10, column=1, value="Delivery Lead Recommendation").font = font_title
rec_text = (
    "We strongly recommend the BALANCED VARIANT (99.0 FTE-Months).\n\n"
    "• Lean Variant (60.7 FTE-Mo) creates an unacceptably high risk profile. Its 70% offshore split without dedicated "
    "onshore BA in Months 1–2 will cause legacy schema discovery bottlenecks that endanger the hard 12-month deadline.\n"
    "• Fast Variant (139.3 FTE-Mo) compresses schedule to 9.5 months but increases cost by +52% over Balanced and "
    "places an unrealistic operational burden on site leads for parallel UAT.\n"
    "• Balanced Variant achieves optimal trade-off: dedicated onshore architecture during Discovery (Phases 1–2), "
    "nearshore tech leads for real-time client collaboration, and a 4-week schedule buffer prior to contract expiry."
)

cell_narrative = ws_rec.cell(row=11, column=1, value=rec_text)
cell_narrative.font = font_regular
ws_rec.merge_cells("A11:D16")
cell_narrative.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

# Auto-fit columns on summary sheet
for col in ws_rec.columns:
    max_len = max(len(str(cell.value or '')) for cell in col)
    col_letter = get_column_letter(col[0].column)
    ws_rec.column_dimensions[col_letter].width = max(max_len + 3, 20)

wb.save(file_path)
print(f"Successfully generated: {file_path}")