import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Directory setup
output_dir = "./modules/1000-management/artefacts/1000-wide"
os.makedirs(output_dir, exist_ok=True)
file_path = os.path.join(output_dir, "04-estimate.xlsx")

wb = openpyxl.Workbook()

# Styles
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E78")
font_subtitle = Font(name="Calibri", size=11, italic=True, color="595959")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=11, bold=True)
font_regular = Font(name="Calibri", size=11)

fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
fill_subtotal = PatternFill(start_color="E9EEF4", end_color="E9EEF4", fill_type="solid")
fill_total = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
fill_contingency = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
fill_margin = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

align_center = Alignment(horizontal="center", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
double_bottom = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='double', color='000000')
)

# -------------------------------------------------------------
# TAB 1: Estimate & Pricing Build
# -------------------------------------------------------------
ws1 = wb.active
ws1.title = "Estimate Summary"

ws1.cell(row=1, column=1, value="EU Machinery Corp — Commercial Delivery Estimate").font = font_title
ws1.cell(row=2, column=1, value="Basis: Balanced Staffing Variant (99 FTE-Months) across 4 Phases").font = font_subtitle

headers1 = ["Line Item / Delivery Component", "Basis / Unit", "Quantity / Rate", "Total Cost (€)"]
for col_idx, h in enumerate(headers1, 1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_center if col_idx > 2 else align_left

estimate_rows = [
    # Base Effort
    ("Phase 1: Discovery & Architecture Foundation", "FTE-Months (Blended)", 11.30, 113000),
    ("Phase 2: Integration Backbone & Portal Build", "FTE-Months (Blended)", 57.00, 570000),
    ("Phase 3: AI Assistant Engine & Regulatory Audit", "FTE-Months (Blended)", 20.75, 207500),
    ("Phase 4: Multi-Site Pilot & Production Cutover", "FTE-Months (Blended)", 9.95, 99500),
    ("SUBTOTAL BASE EFFORT", "99.0 FTE-Mo @ €10,000/mo avg", "", "=SUM(D5:D8)"),
    
    # Delivery Impacts (Broken out)
    ("Ramp-up Productivity Lag Impact", "5% of Base Effort", 0.05, "=D9*0.05"),
    ("Sub-Vendor Coordination (CyberGuard EU)", "3% of Base Effort", 0.03, "=D9*0.03"),
    ("Client Dependency Wait & UAT Buffer", "4% of Base Effort", 0.04, "=D9*0.04"),
    ("SUBTOTAL BASE + DELIVERY IMPACTS", "", "", "=D9+SUM(D10:D12)"),
    
    # Pass-Through & Direct Costs
    ("Outsourced AI Act Compliance Audit (CyberGuard EU)", "Subcontractor Pass-Through", 1, 45000),
    ("Azure AI Search & OpenAI Gateway Inference Reserve", "Gateway Log Sourced (M800)", 1, 25000),
    ("TOTAL DIRECT DELIVERY COST", "", "", "=D13+D14+D15"),
    
    # Risk Contingency vs Margin Separation
    ("Contingency Reserve (Risk Protection)", "15% on Direct Delivery Cost", 0.15, "=D16*0.15"),
    ("TOTAL COST WITH RISK CONTINGENCY", "", "", "=D16+D17"),
    ("Target Commercial Margin (Profit)", "22% Margin on Project Value", 0.22, "=D18*(0.22/(1-0.22))"),
    ("TOTAL FIXED-PRICE PROPOSAL VALUE", "Fixed-Price Milestone Fee", "", "=D18+D19")
]

for idx, (item, basis, qty, formula_val) in enumerate(estimate_rows, 5):
    ws1.cell(row=idx, column=1, value=item).font = font_bold if "TOTAL" in item or "SUBTOTAL" in item else font_regular
    ws1.cell(row=idx, column=2, value=basis).font = font_regular
    
    q_cell = ws1.cell(row=idx, column=3, value=qty)
    q_cell.alignment = align_right
    q_cell.font = font_regular
    
    val_cell = ws1.cell(row=idx, column=4, value=formula_val)
    val_cell.alignment = align_right
    val_cell.number_format = "€#,##0"
    val_cell.font = font_bold if "TOTAL" in item or "SUBTOTAL" in item else font_regular
    
    # Borders & Fills
    for c in range(1, 5):
        ws1.cell(row=idx, column=c).border = thin_border
        
    if "SUBTOTAL" in item:
        for c in range(1, 5):
            ws1.cell(row=idx, column=c).fill = fill_subtotal
    elif "Contingency" in item:
        for c in range(1, 5):
            ws1.cell(row=idx, column=c).fill = fill_contingency
    elif "Margin" in item:
        for c in range(1, 5):
            ws1.cell(row=idx, column=c).fill = fill_margin
    elif "TOTAL FIXED-PRICE" in item:
        for c in range(1, 5):
            ws1.cell(row=idx, column=c).fill = fill_total
            ws1.cell(row=idx, column=c).border = double_bottom

# -------------------------------------------------------------
# TAB 2: Risk Register
# -------------------------------------------------------------
ws2 = wb.create_sheet(title="Risk Register")
ws2.cell(row=1, column=1, value="Delivery Risk Register & Contingency Sizing").font = font_title

headers2 = ["Risk ID", "Risk Description", "Likelihood (1–5)", "Impact (1–5)", "Score (L×I)", "Active Mitigation Strategy", "Contingency Allocation (€)"]
for col_idx, h in enumerate(headers2, 1):
    c = ws2.cell(row=3, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_center if col_idx in [1, 3, 4, 5] else align_left

risks = [
    ("RSK-01", "Undocumented Legacy ERP Middleware Schemas", 4, 4, "=C4*D4", "Mandatory 4-week architectural discovery phase in M1; freeze legacy schemas prior to Phase 2 build.", 45000),
    ("RSK-02", "AI Sales-Ops Quote Hallucination / Pricing Errors", 3, 5, "=C5*D5", "Implement Azure AI Search RAG guardrails, deterministic pricing lookup tables, and mandatory HITL approval for quotes >€5k.", 35000),
    ("RSK-03", "Multi-Site UAT Bottlenecks Across 9 EU Sites", 3, 4, "=C6*D6", "Phased site rollout (Site 1 Pilot, followed by 2 site clusters); mandatory 5-day defect logging SLA.", 30000),
    ("RSK-04", "Third-Party EU AI Act Regulatory Audit Delay", 2, 4, "=C7*D7", "Shift sub-vendor (CyberGuard EU) to continuous checkpoint audits starting Month 6 rather than end-of-project gate.", 25000),
    ("RSK-05", "Azure Landing Zone Admin Access Provisioning Delays", 2, 3, "=C8*D8", "Prerequisite dependency in contract: Azure access required within 10 business days of kickoff.", 15000),
]

for idx, r_data in enumerate(risks, 4):
    for c_idx, val in enumerate(r_data, 1):
        cell = ws2.cell(row=idx, column=c_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 3, 4, 5]:
            cell.alignment = align_center
        if c_idx == 7:
            cell.alignment = align_right
            cell.number_format = "€#,##0"

# Risk Total Row
ws2.cell(row=9, column=1, value="TOTAL SIZED CONTINGENCY").font = font_bold
ws2.cell(row=9, column=7, value="=SUM(G4:G8)").font = font_bold
ws2.cell(row=9, column=7).number_format = "€#,##0"
for c in range(1, 8):
    ws2.cell(row=9, column=c).fill = fill_contingency
    ws2.cell(row=9, column=c).border = double_bottom

# -------------------------------------------------------------
# TAB 3: Assumption Register
# -------------------------------------------------------------
ws3 = wb.create_sheet(title="Assumption Register")
ws3.cell(row=1, column=1, value="Contractual & Delivery Assumptions (Bounded)").font = font_title

headers3 = ["ID", "Category", "Bounded Assumption Statement", "Falsifiable Condition / Threshold", "Impact if Breached"]
for col_idx, h in enumerate(headers3, 1):
    c = ws3.cell(row=3, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_center if col_idx in [1, 2] else align_left

assumptions = [
    ("ASM-01", "Client Resources", "Client provides dedicated legacy ERP domain specialists during Discovery & UAT.", "Minimum 15 hours/week availability in M1–M2 and M10–M12.", "Schedule delay; Change Request for additional EPAM analysis hours."),
    ("ASM-02", "Data Readiness", "Client provides validated, cleansed, machine-readable price books.", "Client PO formal sign-off on cleansed dataset by end of Month 2.", "Phase 3 AI indexing delayed; client bears cleansing remediation costs."),
    ("ASM-03", "Turnaround SLA", "Client site leads review and log UAT defects within agreed SLA window.", "Max 5 business days per site review cycle; unlogged items deemed accepted.", "Site cutover timeline extended; project delay fee applied."),
    ("ASM-04", "Environment", "Azure enterprise tenant with admin privileges is provisioned promptly.", "Full tenant access granted within 10 business days of contract award.", "Day-for-day project milestone shift."),
    ("ASM-05", "Scope Boundaries", "Legacy ERP underlying database schemas remain frozen during development.", "Zero unannounced schema modifications between Month 2 and Month 12.", "API middleware build rework billed under T&M rate card.")
]

for idx, a_data in enumerate(assumptions, 4):
    for c_idx, val in enumerate(a_data, 1):
        cell = ws3.cell(row=idx, column=c_idx, value=val)
        cell.font = font_regular
        cell.border = thin_border
        if c_idx in [1, 2]:
            cell.alignment = align_center

# -------------------------------------------------------------
# TAB 4: Commercial Model Matrix
# -------------------------------------------------------------
ws4 = wb.create_sheet(title="Commercial Model Matrix")
ws4.cell(row=1, column=1, value="Commercial Model Decision & Fit Analysis").font = font_title

headers4 = ["Commercial Model", "RFP Alignment", "Delivery Risk Fit", "Cash-Flow Fit", "Recommendation Status"]
for col_idx, h in enumerate(headers4, 1):
    c = ws4.cell(row=3, column=col_idx, value=h)
    c.font = font_header
    c.fill = fill_header
    c.alignment = align_center if col_idx > 1 else align_left

models = [
    ("Pure Time & Materials (T&M)", "Low (RFP requires fixed-price)", "High (Client carries scope risk, EPAM carries no margin risk)", "Poor (Unpredictable buyer billing)", "REJECTED (Fails RFP Constraint)"),
    ("Pure Capped Fixed-Price", "High (Buyer preferred)", "Low (EPAM carries all legacy discovery risk)", "Good (Predictable milestone payments)", "REJECTED (Unbounded Legacy Risk)"),
    ("Hybrid Milestone Fixed-Price (Gated)", "HIGH (Fully satisfies RFP)", "HIGH (Fixed-price milestones bound by Assumption Register)", "EXCELLENT (Tied to 4 phase exit gates)", "RECOMMENDED COMMERCIAL MODEL")
]

for idx, m_data in enumerate(models, 4):
    for c_idx, val in enumerate(m_data, 1):
        cell = ws4.cell(row=idx, column=c_idx, value=val)
        cell.font = font_bold if "RECOMMENDED" in val else font_regular
        cell.border = thin_border
        if "RECOMMENDED" in val:
            cell.fill = fill_total

# Auto-fit column widths across all sheets
for sheet in wb.worksheets:
    for col in sheet.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        sheet.column_dimensions[col_letter].width = max(max_len + 3, 12)

wb.save(file_path)
print(f"Successfully created: {file_path}")