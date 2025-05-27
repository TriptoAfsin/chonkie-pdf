"""
File utility functions for PDF processing
"""
import os

def get_file_size_kb(file_path):
    """Get file size in KB"""
    return os.path.getsize(file_path) / 1024

def create_chunk_directory(base_dir, filename):
    """Create directory for chunks of a specific file"""
    chunk_dir = os.path.join(base_dir, filename.replace('.pdf', ''))
    os.makedirs(chunk_dir, exist_ok=True)
    return chunk_dir

def find_pdf_files(directory):
    """Find all PDF files in a directory"""
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

def check_files_directory_status(files_dir="files"):
    """
    Check the status of the files directory and return status information
    Returns: (exists, is_empty, pdf_count)
    """
    if not os.path.exists(files_dir):
        return False, True, 0
    
    pdf_files = find_pdf_files(files_dir)
    return True, len(pdf_files) == 0, len(pdf_files)

def display_directory_warnings_and_instructions(files_dir="files"):
    """
    Display warnings and instructions for directory setup
    Returns: True if can proceed, False if should exit
    """
    exists, is_empty, pdf_count = check_files_directory_status(files_dir)
    
    if not exists:
        print(f"\n⚠️  WARNING: '{files_dir}' directory not found!")
        print("📋 SETUP INSTRUCTIONS:")
        print(f"   1. Create a '{files_dir}' directory in the current folder")
        print(f"   2. Place your PDF files inside the '{files_dir}' directory")
        print("   3. Run the application again")
        print("\n💡 Quick setup commands:")
        print(f"   mkdir {files_dir}")
        print(f"   # Then copy your PDF files to the {files_dir} folder")
        return False
    
    if is_empty:
        print(f"\n⚠️  WARNING: '{files_dir}' directory is empty!")
        print("📋 SETUP INSTRUCTIONS:")
        print(f"   1. Place your PDF files inside the '{files_dir}' directory")
        print("   2. Run the application again")
        print(f"\n💡 The '{files_dir}' directory exists but contains no PDF files.")
        return False
    
    # Directory exists and has PDF files
    print(f"✅ Found '{files_dir}' directory with {pdf_count} PDF file(s)")
    return True

def setup_directories(files_dir="files", chunks_dir="chunks"):
    """Setup and validate required directories"""
    # Create chunks directory (this should always work)
    os.makedirs(chunks_dir, exist_ok=True)
    return files_dir, chunks_dir 