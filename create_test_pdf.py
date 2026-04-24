"""
Create a test PDF for testing the summarizer
"""

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    
    def create_test_pdf():
        """Create a test PDF with sample text"""
        filename = "test_sample.pdf"
        
        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph("<b>Artificial Intelligence: A Comprehensive Overview</b>", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # Content
        content = """
        Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the 
        natural intelligence displayed by humans and animals. Leading AI textbooks define the field 
        as the study of intelligent agents: any device that perceives its environment and takes 
        actions that maximize its chance of successfully achieving its goals.
        
        The term artificial intelligence is often used to describe machines that mimic cognitive 
        functions that humans associate with the human mind, such as learning and problem solving. 
        As machines become increasingly capable, tasks considered to require intelligence are often 
        removed from the definition of AI, a phenomenon known as the AI effect.
        
        Modern machine learning techniques are effective at performing a wide range of tasks. 
        Deep learning has dramatically improved the performance of programs in many important 
        subfields of artificial intelligence, including computer vision, speech recognition, 
        image classification, and natural language processing.
        
        AI research has been divided into subfields that often fail to communicate with each other. 
        These sub-fields are based on technical considerations, such as particular goals, the use 
        of particular tools, or the use of particular applications. The traditional goals of AI 
        research include reasoning, knowledge representation, planning, learning, natural language 
        processing, perception, and the ability to move and manipulate objects.
        
        General intelligence is among the field's long-term goals. Approaches include statistical 
        methods, computational intelligence, and traditional symbolic AI. Many tools are used in AI, 
        including versions of search and mathematical optimization, artificial neural networks, and 
        methods based on statistics, probability and economics.
        """
        
        for para in content.split('\n\n'):
            if para.strip():
                p = Paragraph(para.strip(), styles['BodyText'])
                story.append(p)
                story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        print(f"✅ Test PDF created: {filename}")
        print(f"📄 You can now upload this PDF to test the app!")
        return filename
    
    if __name__ == "__main__":
        create_test_pdf()

except ImportError:
    print("⚠️ reportlab not installed")
    print("\nInstall it with: pip install reportlab")
    print("\nOr create a PDF manually and save it as 'test.pdf'")
    print("\n💡 Alternative: Use any existing PDF file to test!")
