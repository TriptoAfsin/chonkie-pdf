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

def setup_directories(files_dir="files", chunks_dir="chunks"):
    """Setup and validate required directories"""
    if not os.path.exists(files_dir):
        raise FileNotFoundError(f"'{files_dir}' directory not found!")
    
    # Create chunks directory
    os.makedirs(chunks_dir, exist_ok=True)
    return files_dir, chunks_dir 