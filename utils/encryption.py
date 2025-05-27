"""
PDF encryption handling utilities
"""
import PyPDF2
from .dependencies import PYCRYPTODOME_AVAILABLE

def is_pdf_encrypted(pdf_path):
    """Check if a PDF file is encrypted"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            return pdf_reader.is_encrypted
    except Exception:
        return False

def handle_encrypted_pdf(pdf_path):
    """Try to handle encrypted PDF files"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if pdf_reader.is_encrypted:
                # Try common passwords
                common_passwords = ['', 'password', '123456', 'admin', 'user']
                
                for password in common_passwords:
                    try:
                        if pdf_reader.decrypt(password):
                            print(f"      ✅ Successfully decrypted with password: '{password}'")
                            return pdf_reader
                    except Exception:
                        continue
                
                print(f"      ❌ PDF is encrypted and requires a password")
                return None
            else:
                return pdf_reader
                
    except Exception as e:
        print(f"      ❌ Error reading PDF: {e}")
        return None

def check_encryption_support():
    """Check if encryption is supported"""
    return PYCRYPTODOME_AVAILABLE 