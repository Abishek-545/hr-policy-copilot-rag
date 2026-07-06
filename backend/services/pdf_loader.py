from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass
class PolicyPage:
    document: str
    page: int
    text: str
    category: str


DOCUMENT_CATEGORIES = {
    "employee_handbook.pdf": "Employee Handbook",
    "remote_work_policy.pdf": "Remote Work",
    "leave_policy.pdf": "Leave and Time Off",
    "travel_expense_policy.pdf": "Travel and Expense",
    "code_of_conduct.pdf": "Code of Conduct",
    "it_security_policy.pdf": "IT Security",
}


DOCUMENT_DESCRIPTIONS = {
    "employee_handbook.pdf": "Core employment standards, onboarding, working hours, pay practices, performance, and workplace expectations.",
    "remote_work_policy.pdf": "Eligibility, hybrid schedules, equipment, communication norms, security, and performance expectations for remote work.",
    "leave_policy.pdf": "Vacation, sick leave, parental leave, bereavement, jury duty, unpaid leave, and request procedures.",
    "travel_expense_policy.pdf": "Business travel approval, reimbursable expenses, receipt rules, per diem guidance, and expense reporting timelines.",
    "code_of_conduct.pdf": "Ethical conduct, respectful workplace standards, conflicts of interest, reporting concerns, and non-retaliation.",
    "it_security_policy.pdf": "Account security, device standards, acceptable use, data protection, incident reporting, and remote access rules.",
}


def load_policy_pages(policy_dir: Path) -> list[PolicyPage]:
    pages: list[PolicyPage] = []
    for pdf_path in sorted(policy_dir.glob("*.pdf")):
        category = DOCUMENT_CATEGORIES.get(pdf_path.name, "General HR Policy")
        with fitz.open(pdf_path) as doc:
            for index, page in enumerate(doc, start=1):
                text = page.get_text("text").strip()
                if text:
                    pages.append(
                        PolicyPage(
                            document=pdf_path.name,
                            page=index,
                            text=text,
                            category=category,
                        )
                    )
    return pages


def get_document_metadata(policy_dir: Path, chunk_counts: dict[str, int]) -> list[dict]:
    metadata = []
    for pdf_path in sorted(policy_dir.glob("*.pdf")):
        with fitz.open(pdf_path) as doc:
            page_count = doc.page_count
        stat = pdf_path.stat()
        metadata.append(
            {
                "name": pdf_path.name,
                "title": pdf_path.stem.replace("_", " ").title(),
                "category": DOCUMENT_CATEGORIES.get(pdf_path.name, "General HR Policy"),
                "pages": page_count,
                "chunks": chunk_counts.get(pdf_path.name, 0),
                "last_indexed": "",
                "description": DOCUMENT_DESCRIPTIONS.get(pdf_path.name, "Policy document used by the HR assistant."),
                "size_kb": round(stat.st_size / 1024, 1),
            }
        )
    return metadata
