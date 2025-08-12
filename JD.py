import google.generativeai as genai
import os
import textwrap
from dotenv import load_dotenv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate

# Load environment variables from .env file
load_dotenv()

def configure_gemini():
    """Configure Gemini API with key from .env file"""
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)

def get_user_input():
    """Collects job details from user input."""
    print("\n  Enter Job Details:")
    job_title = input("Job Title (e.g., 'Senior Data Engineer'): ").strip()
    min_exp = input("Minimum Experience (years): ").strip()
    max_exp = input("Maximum Experience (years): ").strip()
    industry = input("Industry (e.g., 'Fintech'): ").strip()
    
    print("\n Enter 3 Key Responsibilities (1 per line):")
    responsibilities = [input(f"Responsibility {i+1}: ").strip() for i in range(3)]
    
    print("\n Enter Required Tech Stack (comma-separated):")
    tech_stack = [x.strip() for x in input("e.g., Python, SQL, AWS: ").split(',')]
    
    print("\n Enter Tools and Technologies (comma-separated):")
    tools_technologies = [x.strip() for x in input("e.g., Git, JIRA, VS Code: ").split(',')]
    
    print("\n Preferred Skills (comma-separated, or leave blank):")
    preferred_skills = [x.strip() for x in input("e.g., Docker, Kubernetes: ").split(',') if x.strip()]
    
    return {
        "job_title": job_title,
        "min_exp": min_exp,
        "max_exp": max_exp,
        "industry": industry,
        "responsibilities": responsibilities,
        "tech_stack": tech_stack,
        "tools_technologies": tools_technologies,
        "preferred_skills": preferred_skills,
    }

def generate_jd_with_gemini(job_details):
    """Generates JD using Gemini AI."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Generate a professional Job Description that begins with "We are looking for..." and includes the following details:
        
        Position: {job_details['job_title']}
        Experience: {job_details['min_exp']}-{job_details['max_exp']} years
        Industry: {job_details['industry']}

        Key Responsibilities:
        1. {job_details['responsibilities'][0]}
        2. {job_details['responsibilities'][1]}
        3. {job_details['responsibilities'][2]}

        Required Technical Skills:
        - {", ".join(job_details['tech_stack'])}

        Tools and Technologies:
        - {", ".join(job_details['tools_technologies'])}

        Preferred Skills:
        - {", ".join(job_details['preferred_skills']) if job_details['preferred_skills'] else "None"}

        Formatting Requirements:
        - Start with "We are looking for..."
        - Use professional but engaging tone
        - Organize in clear sections with bullet points
        - Keep technical descriptions precise
        - Exclude company information and soft skills
        - Use proper markdown formatting
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating JD: {str(e)}")
        return None

def generate_questionnaire(job_details, difficulty, num_questions):
    """Generates technical questions based on JD content."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Generate {num_questions} technical interview questions for a {job_details['job_title']} position.
        Difficulty Level: {difficulty}
        
        Based on these job requirements:
        - Key Skills: {', '.join(job_details['tech_stack'] + job_details['tools_technologies'])}
        - Responsibilities: {', '.join(job_details['responsibilities'])}
        - Preferred Skills: {', '.join(job_details['preferred_skills']) if job_details['preferred_skills'] else "None"}
        
        Question Requirements:
        - Focus on technical concepts
        - Include {difficulty}-level questions
        - Cover all key technologies mentioned
        - Include practical/scenario-based questions
        - Format as numbered list with clear questions
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating questions: {str(e)}")
        return None

def save_to_pdf(content, filename):
    """Saves content to a properly formatted PDF file."""
    try:
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            leftMargin=40,
            rightMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        for line in content.splitlines():
            if line.strip() == "":
                continue
                
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                p = Paragraph(line, styles["Normal"])
            elif line.strip().startswith("- "):
                p = Paragraph("• " + line[2:], styles["Normal"])
            else:
                p = Paragraph(line, styles["Heading2"])
            
            story.append(p)
        
        doc.build(story)
        print(f"Content saved to {filename}")
    except Exception as e:
        print(f"Error saving to PDF: {str(e)}")

if __name__ == "__main__":
    try:
        configure_gemini()
        job_details = get_user_input()
        
        # Generate JD
        jd = generate_jd_with_gemini(job_details)
        if jd:
            print("\n Generated Job Description:\n")
            print(jd)
            
            # Save JD to PDF
            jd_filename = f"JD_{job_details['job_title'].replace(' ', '_')}.pdf"
            save_to_pdf(jd, jd_filename)
            
            # Generate Questionnaire
            print("\n Questionnaire Generator")
            difficulty = input("Choose difficulty (Easy/Medium/Advanced): ").capitalize()
            while difficulty not in ["Easy", "Medium", "Advanced"]:
                print("Please enter Easy, Medium, or Advanced")
                difficulty = input("Choose difficulty (Easy/Medium/Advanced): ").capitalize()
            
            num_questions = int(input("Number of questions to generate (5-20): "))
            num_questions = max(5, min(20, num_questions))  # Clamp between 5-20
            
            questions = generate_questionnaire(job_details, difficulty, num_questions)
            if questions:
                print(f"\n {difficulty} Technical Questions ({num_questions}):\n")
                print(questions)
                
                # Save questions to PDF
                questions_filename = f"Questions_{job_details['job_title'].replace(' ', '_')}_{difficulty}.pdf"
                save_to_pdf(questions, questions_filename)
        else:
            print("Failed to generate job description")
    except Exception as e:
        print(f"Error: {str(e)}")