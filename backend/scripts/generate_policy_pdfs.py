from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "policies"
COMPANY = "Northstar Mobility"


POLICIES = {
    "employee_handbook.pdf": {
        "title": "Employee Handbook",
        "category": "Core Employment Standards",
        "owner": "People Operations",
        "sections": [
            ("Welcome and Purpose", [
                "This handbook explains the everyday employment standards for Northstar Mobility employees. It is written for clarity, consistency, and employee self-service.",
                "The handbook applies to regular full-time, regular part-time, intern, temporary, and fixed-term employees unless a section states otherwise.",
                "Employees use this handbook as the first reference for workplace expectations and contact People Operations when policy details are unclear."
            ]),
            ("Employment Classification", [
                "Full-time employees are regularly scheduled to work 40 hours per week and are eligible for the full benefits program, subject to plan terms.",
                "Part-time employees are regularly scheduled to work fewer than 30 hours per week. Eligibility for selected benefits is determined by local law and the official benefit plan terms.",
                "Temporary and intern assignments are time-limited and do not guarantee conversion to regular employment."
            ]),
            ("Probation and Introductory Period", [
                "New regular employees complete a 90-day introductory period. The period is used to confirm role fit, work quality, attendance, collaboration, and alignment with company values.",
                "Managers provide documented feedback at approximately 30, 60, and 90 days. Successful completion does not change at-will employment status where applicable.",
                "The introductory period can be extended up to 60 additional days when performance, attendance, or training completion requires more review."
            ]),
            ("Working Hours and Attendance", [
                "Standard office hours are Monday through Friday, 9:00 a.m. to 5:30 p.m. local time, with adjustments for approved shift schedules or regional requirements.",
                "Employees are expected to be ready to work at the start of their scheduled day, attend required meetings, and notify their manager as soon as possible when delayed or absent.",
                "Repeated unscheduled absences, late arrivals, or missed meetings may result in coaching, corrective action, or additional attendance controls."
            ]),
            ("Pay Practices", [
                "Employees are paid according to the payroll calendar published by Payroll Operations. Non-exempt employees must accurately record all hours worked.",
                "Overtime for non-exempt employees must be approved in advance. Unapproved overtime must still be reported and will be paid according to law.",
                "Employees submit pay questions to Payroll within five business days of the pay date so corrections can be reviewed promptly."
            ]),
            ("Performance Management", [
                "Performance is evaluated through goal progress, quality of work, ownership, collaboration, customer impact, and adherence to company policies.",
                "Formal performance reviews occur at least annually. Managers also conduct quarterly check-ins when needed for goal alignment and development planning.",
                "Performance improvement plans are used when expectations are not met and structured support is appropriate. The plan identifies gaps, required outcomes, support resources, and review dates."
            ]),
            ("Benefits Overview", [
                "Eligible employees can participate in health, dental, vision, retirement, life insurance, disability, wellness, and employee assistance programs.",
                "Benefit eligibility, waiting periods, and employee contributions are governed by the official plan documents.",
                "Employees must complete benefit elections within 30 days of eligibility or wait until the next open enrollment period unless they experience a qualifying life event."
            ]),
            ("Workplace Conduct", [
                "Employees are expected to communicate respectfully, protect confidential information, follow safety rules, and use company resources responsibly.",
                "Bullying, harassment, discrimination, retaliation, falsification of records, theft, threats, or intentional policy violations are prohibited.",
                "Employees can report concerns to a manager, People Operations, Legal, Security, or the ethics reporting channel."
            ]),
            ("Corrective Action", [
                "Corrective action can include coaching, verbal warning, written warning, final warning, suspension, or termination depending on the situation.",
                "Northstar can skip corrective action steps when conduct is serious, creates risk, or violates law or safety requirements.",
                "Employees are expected to participate honestly in investigations and corrective discussions."
            ]),
            ("Separation and Exit Process", [
                "Employees who resign are asked to provide at least two weeks of written notice so the company can plan transition coverage.",
                "Company property must be returned by the final working day, including laptops, badges, access cards, mobile devices, documents, and equipment.",
                "Final pay, benefit continuation, and unused vacation payout are handled according to applicable law and company policy."
            ])
        ],
        "table": [["Topic", "Standard"], ["Introductory period", "90 days"], ["Standard week", "40 hours"], ["Benefit election window", "30 days"], ["Resignation notice", "2 weeks preferred"]]
    },
    "remote_work_policy.pdf": {
        "title": "Remote Work Policy",
        "category": "Hybrid and Remote Work",
        "owner": "People Operations and IT",
        "sections": [
            ("Purpose", [
                "This policy defines how eligible employees may work remotely while maintaining productivity, data security, collaboration, and employee well-being.",
                "Remote work is a work arrangement, not a separate benefit guarantee. Business needs, role requirements, performance, and security obligations determine eligibility.",
                "Approved remote work can be hybrid, occasional, temporary, or fully remote depending on the role and written approval."
            ]),
            ("Eligibility", [
                "Employees must have satisfactory performance, reliable attendance, a role suitable for remote work, and a secure work environment.",
                "Roles requiring physical equipment, secure labs, direct facilities support, or on-site customer operations are limited or ineligible unless leadership approves an exception.",
                "New employees become eligible for recurring remote work after the introductory period unless the offer letter states otherwise."
            ]),
            ("Hybrid Schedule", [
                "Hybrid employees are expected to work on-site at least three days per week unless their department has an approved exception.",
                "Core collaboration hours are 10:00 a.m. to 3:00 p.m. local team time. Employees must be reachable during core hours.",
                "Managers can require in-office attendance for onboarding, planning, performance meetings, customer events, audits, or urgent business needs."
            ]),
            ("Approval Process", [
                "Employees request remote work through the HR service portal with proposed schedule, location, equipment needs, and manager approval.",
                "Recurring arrangements must be reviewed at least every six months. Changes in role, performance, location, or team needs may require reapproval.",
                "Remote work from another country or state requires advance approval from People Operations, Tax, Legal, and IT Security."
            ]),
            ("Workspace and Equipment", [
                "Employees must maintain a safe, quiet, and ergonomically suitable workspace with reliable internet.",
                "Company laptops, approved monitors, headsets, and security tools must be used for company work. Personal devices may not store confidential company data.",
                "Employees are responsible for normal home utility costs unless a written regional policy provides otherwise."
            ]),
            ("Communication Standards", [
                "Employees must keep calendar availability current, attend required meetings, respond to messages within reasonable business time, and use video for high-context discussions when it improves clarity.",
                "Team decisions, action items, and approvals are documented in shared systems so remote and on-site employees have equal access to information.",
                "Managers set clear expectations for response times, meeting norms, and focus work blocks."
            ]),
            ("Security Requirements", [
                "Remote employees must use VPN or approved zero-trust access where required, lock screens when away, and protect devices from family members, visitors, and unauthorized users.",
                "Confidential discussions should not be held in public areas where they can be overheard.",
                "Printed confidential material at home must be minimized and shredded when no longer needed."
            ]),
            ("Performance and Availability", [
                "Remote employees are measured by outcomes, quality, collaboration, timeliness, and policy compliance.",
                "Remote work can be modified or revoked when performance, attendance, responsiveness, confidentiality, or collaboration expectations are not met.",
                "Employees must not provide dependent care as a substitute for working time during scheduled hours."
            ]),
            ("Travel to Office", [
                "Employees who choose to live far from their assigned office are normally responsible for travel costs to attend required on-site meetings.",
                "Company-paid travel may be approved when the business specifically requires an employee to travel from an approved remote work location.",
                "Travel time and expense reimbursement follow the Travel and Expense Policy."
            ]),
            ("Health and Safety", [
                "Employees must report work-related injuries that occur during remote work hours immediately to their manager and People Operations.",
                "Remote workspaces may be reviewed through self-certification or virtual assessment when required for safety, security, or accommodation reasons.",
                "Employees should take meal and rest breaks consistent with local law and company guidance."
            ])
        ],
        "table": [["Requirement", "Standard"], ["On-site expectation", "3 days per week for hybrid roles"], ["Core hours", "10:00 a.m. to 3:00 p.m."], ["Review cycle", "Every 6 months"], ["International remote work", "Advance approval required"]]
    },
    "leave_policy.pdf": {
        "title": "Leave Policy",
        "category": "Leave and Time Off",
        "owner": "People Operations",
        "sections": [
            ("Purpose and Scope", [
                "This policy explains paid and unpaid leave programs available to eligible employees.",
                "Leave benefits can differ by country, state, province, union agreement, or statutory requirement. When law provides greater benefits, the legal requirement controls.",
                "Employees submit leave requests as early as possible so managers can plan coverage."
            ]),
            ("Vacation Leave", [
                "Regular full-time employees accrue 15 vacation days per calendar year during their first, second, and third years of continuous employment.",
                "Beginning on the first day of the fourth year of continuous employment, regular full-time employees accrue 20 vacation days per calendar year.",
                "Employees request vacation at least two weeks in advance for absences of three or more consecutive business days."
            ]),
            ("Sick Leave", [
                "Regular full-time employees receive 10 paid sick days per calendar year, available for personal illness, preventive care, medical appointments, or care of an eligible family member.",
                "Employees notify their manager before the start of the workday when using unscheduled sick leave.",
                "Medical certification may be required for absences longer than three consecutive workdays or when allowed by law."
            ]),
            ("Holidays", [
                "Northstar publishes the annual holiday calendar before the start of each calendar year.",
                "Employees required to work on a company holiday may receive holiday pay, an alternate day off, or another arrangement based on role classification and local law.",
                "Floating holidays may be used for personal, cultural, religious, or wellness observances with manager approval."
            ]),
            ("Parental Leave", [
                "Eligible birth, adoptive, and foster parents may receive up to 12 weeks of job-protected parental leave.",
                "Primary caregivers may be eligible for up to 8 weeks of paid parental leave. Non-primary caregivers may be eligible for up to 4 weeks of paid parental leave.",
                "Employees provide at least 30 days of notice when the need for parental leave is foreseeable."
            ]),
            ("Bereavement Leave", [
                "Employees may take up to 5 paid business days after the death of an immediate family member.",
                "Employees may take up to 2 paid business days after the death of an extended family member.",
                "Additional unpaid time or vacation may be approved for travel, estate matters, cultural practices, or exceptional circumstances."
            ]),
            ("Jury Duty and Witness Leave", [
                "Employees summoned for jury duty or required court witness service should notify their manager and People Operations as soon as possible.",
                "The company will provide paid jury duty leave for up to 10 business days unless local law requires more.",
                "Employees should return to work when released early from court service during normal working hours."
            ]),
            ("Medical and Family Leave", [
                "Employees may be eligible for statutory medical or family leave programs based on location, tenure, hours worked, and qualifying reason.",
                "People Operations will provide required notices, certification forms, and benefit continuation guidance.",
                "Employees must cooperate with reasonable certification, recertification, and return-to-work requirements."
            ]),
            ("Unpaid Personal Leave", [
                "Unpaid personal leave may be approved when business needs allow and paid leave options are exhausted or not applicable.",
                "Requests must explain the reason, expected duration, and proposed return date.",
                "Benefits during unpaid leave depend on plan terms and applicable law."
            ]),
            ("Return from Leave", [
                "Employees must confirm their return date with their manager and People Operations before returning from leave.",
                "A fitness-for-duty certification may be required when returning from medical leave if permitted by law.",
                "Failure to return from approved leave without communication may be treated as job abandonment."
            ])
        ],
        "table": [["Leave Type", "Standard"], ["Vacation", "15 days per year during the first 3 years of service; 20 days per year starting in the fourth year of service"], ["Sick leave", "10 paid days per year"], ["Parental leave", "Up to 12 weeks"], ["Bereavement", "Up to 5 paid days"]]
    },
    "travel_expense_policy.pdf": {
        "title": "Travel and Expense Policy",
        "category": "Business Travel and Reimbursement",
        "owner": "Finance Operations",
        "sections": [
            ("Purpose", [
                "This policy explains how employees plan business travel, spend company funds, and request reimbursement.",
                "Employees are expected to spend responsibly, choose cost-effective options, and submit accurate expenses on time.",
                "Managers approve expenses based on business purpose, policy compliance, receipts, and budget availability."
            ]),
            ("Travel Approval", [
                "Overnight travel requires manager approval before booking. International travel also requires director approval and travel security review.",
                "Travel must be booked through the approved travel platform unless Finance Operations grants an exception.",
                "Employees book at least 14 days in advance when the business schedule allows it to reduce cost."
            ]),
            ("Air Travel", [
                "Economy class is required for flights under six hours. Premium economy may be approved for flights of six hours or more.",
                "Business class requires vice president approval and is generally limited to flights exceeding ten hours or documented medical accommodation.",
                "Employees may keep personal loyalty points when participation does not increase company cost."
            ]),
            ("Lodging", [
                "Employees choose safe, business-appropriate hotels near the work location and within published city rate guidance.",
                "Luxury hotels, suites, resort fees unrelated to business, and in-room entertainment are not reimbursable.",
                "Employees use preferred hotels when available unless location, safety, or cost makes another option more reasonable."
            ]),
            ("Meals and Per Diem", [
                "Reasonable meals during business travel are reimbursable up to local daily guidance. Alcohol is reimbursable only with director approval and legitimate business purpose.",
                "When meals are provided by a conference, hotel, airline, or host, employees must not claim a duplicate meal expense.",
                "Tips must be reasonable and consistent with local customs."
            ]),
            ("Ground Transportation", [
                "Employees use public transit, shuttle, rideshare, taxi, rental car, or personal vehicle based on cost, safety, and business need.",
                "Rental cars require manager approval unless they are clearly less expensive than other options or necessary for the business itinerary.",
                "Personal vehicle mileage is reimbursed at the published company mileage rate and requires route documentation."
            ]),
            ("Reimbursable Expenses", [
                "Reimbursable expenses include approved transportation, lodging, business meals, conference fees, visa fees, required vaccinations, baggage fees, parking, and business communication charges.",
                "Non-reimbursable expenses include commuting, fines, personal entertainment, gym fees, minibar charges, clothing, childcare, pet care, and optional upgrades.",
                "Expenses must have a clear business purpose and be supported by receipts when required."
            ]),
            ("Receipts and Submissions", [
                "Receipts are required for expenses of 25 USD or more unless local law or finance guidance sets a lower threshold.",
                "Expense reports must be submitted within 10 business days after completing travel or incurring the expense.",
                "Missing receipt affidavits may be used occasionally but repeated missing receipts may result in reimbursement delays or denial."
            ]),
            ("Corporate Card Use", [
                "Corporate cards may be used only for authorized business expenses. Personal use is prohibited.",
                "Employees must reconcile card charges by the monthly deadline and attach required receipts.",
                "Lost cards, suspected fraud, or incorrect charges must be reported immediately to Finance Operations."
            ]),
            ("Policy Exceptions", [
                "Exceptions require written approval from Finance Operations before the expense is incurred whenever possible.",
                "Emergency exceptions may be approved after the fact when employee safety, travel disruption, or business continuity requires immediate action.",
                "Managers may not approve their own expenses."
            ])
        ],
        "table": [["Expense Rule", "Standard"], ["Book travel", "At least 14 days ahead when the business schedule allows"], ["Receipt threshold", "25 USD"], ["Expense deadline", "10 business days"], ["International travel", "Director approval required"]]
    },
    "code_of_conduct.pdf": {
        "title": "Code of Conduct",
        "category": "Ethics and Workplace Conduct",
        "owner": "Legal and People Operations",
        "sections": [
            ("Our Commitment", [
                "Northstar Mobility is committed to lawful, ethical, respectful, and accountable business conduct.",
                "Every employee is responsible for acting with integrity, speaking up about concerns, and protecting the trust of colleagues, customers, suppliers, and communities.",
                "Leaders have an additional responsibility to model ethical behavior and respond promptly to concerns."
            ]),
            ("Respectful Workplace", [
                "Employees must treat colleagues, candidates, customers, vendors, and visitors with respect and professionalism.",
                "Harassment, discrimination, bullying, intimidation, slurs, unwanted conduct, or exclusion based on protected characteristics are prohibited.",
                "Employees report behavior that undermines a safe and inclusive workplace."
            ]),
            ("Anti-Harassment and Non-Discrimination", [
                "The company prohibits harassment or discrimination based on legally protected characteristics, including race, color, religion, sex, pregnancy, sexual orientation, gender identity, national origin, age, disability, veteran status, genetic information, or any other protected status.",
                "Prohibited harassment can be verbal, physical, visual, written, digital, or environmental.",
                "Managers who receive a concern must promptly notify People Operations or Legal."
            ]),
            ("Conflicts of Interest", [
                "Employees must avoid situations where personal interests conflict or appear to conflict with company interests.",
                "Examples include supervising a relative, accepting improper gifts, holding outside employment that interferes with company duties, or having a financial interest in a supplier decision.",
                "Potential conflicts must be disclosed through the conflict disclosure process before the employee acts on the matter."
            ]),
            ("Gifts and Business Courtesies", [
                "Employees may accept modest business courtesies that are infrequent, lawful, transparent, and not intended to influence decisions.",
                "Cash, cash equivalents, lavish gifts, and gifts during active procurement decisions are prohibited.",
                "Government official interactions are subject to stricter anti-corruption rules and require Legal guidance."
            ]),
            ("Confidential Information", [
                "Employees must protect confidential business information, employee data, customer data, technical information, pricing, strategy, and unreleased product plans.",
                "Confidential information may be shared only with authorized people who have a legitimate business need.",
                "Confidentiality obligations continue after employment ends."
            ]),
            ("Accurate Records", [
                "Employees must create and maintain accurate business records, including time records, expense reports, quality records, financial data, and customer documentation.",
                "Falsifying records, hiding errors, backdating approvals, or misclassifying expenses is prohibited.",
                "Records must be retained or disposed of according to the records retention schedule and legal hold notices."
            ]),
            ("Reporting Concerns", [
                "Employees may report concerns to their manager, People Operations, Legal, Security, Internal Audit, or the ethics reporting channel.",
                "Reports may be made anonymously where permitted by law.",
                "Employees provide as much detail as possible, including dates, names, documents, and relevant systems."
            ]),
            ("Non-Retaliation", [
                "Northstar prohibits retaliation against anyone who raises a concern in good faith, participates in an investigation, or refuses to engage in improper conduct.",
                "Retaliation includes termination, demotion, schedule changes, threats, exclusion, intimidation, or other adverse treatment because of protected reporting activity.",
                "Suspected retaliation should be reported immediately."
            ]),
            ("Investigations and Accountability", [
                "The company reviews reported concerns fairly, promptly, and as confidentially as practical.",
                "Employees must cooperate honestly in investigations and must not interfere with evidence, witnesses, or systems.",
                "Violations may result in corrective action up to and including termination."
            ])
        ],
        "table": [["Concern Type", "Reporting Channel"], ["Harassment", "Manager or People Operations"], ["Ethics issue", "Ethics reporting channel"], ["Security concern", "Security team"], ["Legal issue", "Legal department"]]
    },
    "it_security_policy.pdf": {
        "title": "IT Security Policy",
        "category": "Information Security",
        "owner": "Information Security",
        "sections": [
            ("Purpose", [
                "This policy defines employee responsibilities for protecting company systems, data, devices, and accounts.",
                "Information security is a shared responsibility. Employees must use approved tools and report suspicious activity quickly.",
                "Policy violations may create legal, operational, financial, and reputational risk."
            ]),
            ("Account Security", [
                "Employees must use unique company passwords and multi-factor authentication for company systems.",
                "Passwords may not be shared, reused from personal accounts, written in visible locations, or sent through chat or email.",
                "Employees must report suspected account compromise immediately to the Service Desk and Information Security."
            ]),
            ("Device Standards", [
                "Company work must be performed on managed devices unless a written exception is approved by IT.",
                "Managed devices must run current security software, disk encryption, endpoint protection, and required operating system updates.",
                "Lost or stolen devices must be reported within one hour of discovery."
            ]),
            ("Acceptable Use", [
                "Company systems are provided for business purposes and limited reasonable personal use that does not interfere with work or create risk.",
                "Employees may not use company systems for illegal activity, harassment, unauthorized monitoring, cryptocurrency mining, pirated content, or offensive material.",
                "The company may monitor systems as permitted by law to protect security, compliance, and operations."
            ]),
            ("Data Classification", [
                "Company data is classified as Public, Internal, Confidential, or Restricted.",
                "Confidential and Restricted data must be stored only in approved systems with access limited to business need.",
                "Restricted data includes government identifiers, payment data, health information, credentials, trade secrets, unreleased financials, and sensitive employee records."
            ]),
            ("Email and Phishing", [
                "Employees must inspect unexpected links, attachments, payment requests, credential prompts, and urgent external messages.",
                "Suspected phishing must be reported using the approved reporting button or sent to the Security Operations mailbox.",
                "Employees must not forward suspicious messages to colleagues except through the approved reporting process."
            ]),
            ("Remote Access", [
                "Remote access must use approved VPN, zero-trust gateway, or managed access tools.",
                "Employees may not bypass security controls, disable endpoint protection, or connect unmanaged storage devices without approval.",
                "Public Wi-Fi may be used only with approved secure access controls."
            ]),
            ("Software and Cloud Tools", [
                "Employees may install only approved software or browser extensions on company devices.",
                "New cloud tools that store, process, or transmit company data require security and procurement review before use.",
                "Source code, customer data, and confidential documents may not be pasted into unapproved AI tools."
            ]),
            ("Incident Reporting", [
                "Security incidents include lost devices, suspected phishing, malware alerts, accidental data sharing, unauthorized access, credential exposure, and suspicious system behavior.",
                "Employees must report security incidents immediately, even if they are unsure whether harm occurred.",
                "Employees must not investigate incidents on their own beyond preserving evidence and following Security instructions."
            ]),
            ("Access Reviews and Offboarding", [
                "System owners must review access periodically and remove access that is no longer needed.",
                "Managers must notify IT promptly when employees transfer roles, change responsibilities, or separate from the company.",
                "Departing employees must return devices, badges, tokens, and other company assets by the final working day."
            ])
        ],
        "table": [["Security Requirement", "Standard"], ["MFA", "Required"], ["Lost device report", "Within 1 hour"], ["Data classes", "Public, Internal, Confidential, Restricted"], ["AI tools", "Approved tools only"]]
    }
}


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(0.7 * inch, 0.45 * inch, f"{COMPANY} - Internal Policy")
    canvas.drawRightString(7.8 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(filename: str, policy: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="PolicyTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=28, textColor=colors.HexColor("#0f172a"), spaceAfter=16))
    styles.add(ParagraphStyle(name="SectionTitle", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#1d4ed8"), spaceBefore=10, spaceAfter=8))
    styles.add(ParagraphStyle(name="BodyPolicy", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, textColor=colors.HexColor("#1f2937"), spaceAfter=7))
    styles.add(ParagraphStyle(name="Meta", parent=styles["BodyText"], fontName="Helvetica", fontSize=9, leading=13, textColor=colors.HexColor("#475569"), spaceAfter=5))

    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.75 * inch,
    )
    story = [
        Paragraph(policy["title"], styles["PolicyTitle"]),
        Paragraph(f"Company: {COMPANY}", styles["Meta"]),
        Paragraph(f"Category: {policy['category']}", styles["Meta"]),
        Paragraph(f"Policy Owner: {policy['owner']}", styles["Meta"]),
        Paragraph("Effective Date: January 1, 2026", styles["Meta"]),
        Paragraph("Document Type: Employee-facing HR policy reference", styles["Meta"]),
        Spacer(1, 0.2 * inch),
    ]

    table = Table(policy["table"], hAlign="LEFT", colWidths=[2.2 * inch, 4.7 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dbeafe")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([table, Spacer(1, 0.22 * inch)])

    for index, (heading, paragraphs) in enumerate(policy["sections"], start=1):
        story.append(Paragraph(f"{index}. {heading}", styles["SectionTitle"]))
        for paragraph in paragraphs:
            story.append(Paragraph(paragraph, styles["BodyPolicy"]))
        story.append(Paragraph("Employee guidance: keep related approvals, requests, receipts, or reports in the designated company system so decisions can be reviewed consistently.", styles["BodyPolicy"]))
        story.append(Paragraph("Manager guidance: managers must apply this policy consistently, document exceptions, and consult the policy owner before approving any action that could create compliance, pay, privacy, security, or employee-relations risk.", styles["BodyPolicy"]))
        story.append(Paragraph("Review standard: policy questions should be resolved using the current HR policy library, applicable law, and written guidance from the policy owner. Informal past practice does not override the approved policy.", styles["BodyPolicy"]))
        story.append(Spacer(1, 0.1 * inch))

    story.append(PageBreak())
    story.append(Paragraph("Acknowledgement and Questions", styles["SectionTitle"]))
    story.append(Paragraph("Employees are responsible for reading this policy and following the standards that apply to their role and location. Questions should be directed to the policy owner or People Operations before taking action when requirements are unclear.", styles["BodyPolicy"]))
    story.append(Paragraph("This policy may be updated periodically. The current approved version in the HR policy library controls over printed or downloaded copies.", styles["BodyPolicy"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def main() -> None:
    for filename, policy in POLICIES.items():
        build_pdf(filename, policy)
        print(f"generated {filename}")


if __name__ == "__main__":
    main()
