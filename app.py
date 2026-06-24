import streamlit as st
import pytesseract
from docx import Document
from PIL import Image
import io

# Optional: If you are on Windows and Tesseract isn't in your PATH, uncomment & point to it:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Image to DOCX Converter", page_icon="📝")
st.title("📝 Multi-Image Text Extractor to DOCX")
st.write("Upload your images below. This updated version forces left-to-right paragraph reading.")

uploaded_files = st.file_uploader(
    "Choose images...", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Loaded {len(uploaded_files)} image(s).")
    
    doc = Document()
    doc.add_heading('Extracted Text Document', level=0)
    
    if st.button("Extract Text & Generate DOCX"):
        progress_bar = st.progress(0)
        
        for index, file in enumerate(uploaded_files):
            image = Image.open(file)
            
            st.subheader(f"📄 Processing: {file.name}")
            st.image(image, use_container_width=True)
            
            with st.spinner(f"Reading text from {file.name}..."):
                # config='--psm 3' tells tesseract to automatically detect a full block of text
                # config='--psm 6' assumes a single uniform block of text
                extracted_text = pytesseract.image_to_string(image, config='--psm 3')
            
            if extracted_text.strip():
                st.text_area(f"Extracted from {file.name}:", extracted_text, height=250)
                
                doc.add_heading(f"Source: {file.name}", level=2)
                doc.add_paragraph(extracted_text)
                doc.add_page_break()
            else:
                st.warning(f"No clear text detected in {file.name}.")
                
            progress_bar.progress((index + 1) / len(uploaded_files))
            
        doc_buffer = io.BytesIO()
        doc.save(doc_buffer)
        doc_buffer.seek(0)
        
        st.success("🎉 All images processed successfully!")
        
        st.download_button(
            label="📥 Download Word Document (.docx)",
            data=doc_buffer,
            file_name="extracted_text.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )