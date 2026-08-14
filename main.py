import os
from crewai import Crew, Process
from agents import research_agent, analysis_agent, report_agent
from tasks import create_tasks
from pdf_generator import markdown_to_pdf

def run_intelligence_report(company_name: str):
    print(f"\n Starting intelligence report for: {company_name}\n")
    tasks = create_tasks(company_name)
    crew = Crew(
        agents = [research_agent, analysis_agent, report_agent],
        tasks = tasks,
        process = Process.sequential,
        verbose = True,
    )
    result = crew.kickoff()
    output_path = f"outputs/{company_name.lower().replace(' ', '_')}_report.pdf"
    markdown_to_pdf(str(result), output_path, company_name)
    return result

if __name__ == "__main__":
    company = input("Enter company or startup name: ").strip()
    run_intelligence_report(company)