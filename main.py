"""
PDF Chunking Tool with Compression - Refactored Version
Main entry point for the application
"""
import os
import PyPDF2
from datetime import datetime
from pathlib import Path

# Import our custom modules
from utils.dependencies import print_dependency_status
from utils.file_utils import find_pdf_files, setup_directories, get_file_size_kb
from utils.encryption import is_pdf_encrypted, handle_encrypted_pdf, check_encryption_support
from utils.chunker import chunk_pdf_by_pages
from utils.reporter import generate_report
from utils.user_input import get_chunk_size, get_compression_settings

def process_pdf_files(pdf_files, files_dir, chunks_dir, max_size_kb, compress_chunks, compression_quality):
    """Process all PDF files and return chunking information"""
    all_chunks_info = {}
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n📋 Progress: {i}/{len(pdf_files)}")
        pdf_path = os.path.join(files_dir, pdf_file)
        
        try:
            original_size = get_file_size_kb(pdf_path)
            
            # Check if PDF is encrypted first
            if is_pdf_encrypted(pdf_path) and not check_encryption_support():
                print(f"   🔒 Skipping encrypted PDF (PyCryptodome not available)")
                all_chunks_info[pdf_file] = {
                    'filename': pdf_file,
                    'original_size': original_size,
                    'total_pages': 0,
                    'chunks': [],
                    'status': 'Skipped: Encrypted PDF requires PyCryptodome'
                }
                continue
            
            # Get total pages for reporting
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Handle encryption if needed
                if pdf_reader.is_encrypted:
                    decrypted_reader = handle_encrypted_pdf(pdf_path)
                    if decrypted_reader is None:
                        all_chunks_info[pdf_file] = {
                            'filename': pdf_file,
                            'original_size': original_size,
                            'total_pages': 0,
                            'chunks': [],
                            'status': 'Failed: Could not decrypt PDF'
                        }
                        continue
                    pdf_reader = decrypted_reader
                
                total_pages = len(pdf_reader.pages)
            
            # Process the PDF file
            chunks = chunk_pdf_by_pages(pdf_path, max_size_kb, chunks_dir, compress_chunks, compression_quality)
            
            all_chunks_info[pdf_file] = {
                'filename': pdf_file,
                'original_size': original_size,
                'total_pages': total_pages,
                'chunks': chunks,
                'status': 'Success' if chunks else 'Failed'
            }
            
        except Exception as e:
            print(f"   ❌ Failed to process {pdf_file}: {str(e)}")
            all_chunks_info[pdf_file] = {
                'filename': pdf_file,
                'original_size': 0,
                'total_pages': 0,
                'chunks': [],
                'status': f'Error: {str(e)}'
            }
    
    return all_chunks_info

def main():
    """Main function to run the PDF chunking tool"""
    # ASCII Art for Chonkie PDF
    print("""
 ██████╗██╗  ██╗ ██████╗ ███╗   ██╗██╗  ██╗██╗███████╗    ██████╗ ██████╗ ███████╗
██╔════╝██║  ██║██╔═══██╗████╗  ██║██║ ██╔╝██║██╔════╝    ██╔══██╗██╔══██╗██╔════╝
██║     ███████║██║   ██║██╔██╗ ██║█████╔╝ ██║█████╗      ██████╔╝██║  ██║█████╗  
██║     ██╔══██║██║   ██║██║╚██╗██║██╔═██╗ ██║██╔══╝      ██╔═══╝ ██║  ██║██╔══╝  
╚██████╗██║  ██║╚██████╔╝██║ ╚████║██║  ██╗██║███████╗    ██║     ██████╔╝██║     
 ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝╚══════╝    ╚═╝     ╚═════╝ ╚═╝     

                           by Afshin Nahian Tripto
                          GitHub: TriptoAfsin
    """)
    print("🚀 Chonkie PDF Started")
    print("=" * 60)
    
    # Show available compression libraries
    print_dependency_status()
    
    # Get user preferences
    max_size_kb = get_chunk_size()
    compress_chunks, compression_quality = get_compression_settings()
    
    # Setup directories
    try:
        files_dir, chunks_dir = setup_directories()
        print(f"📁 Chunks will be saved in: {chunks_dir}")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return
    
    # Find all PDF files
    pdf_files = find_pdf_files(files_dir)
    
    if not pdf_files:
        print(f"❌ No PDF files found in '{files_dir}' directory!")
        return
    
    print(f"\n🔍 Found {len(pdf_files)} PDF files to process")
    print(f"📊 Maximum chunk size: {max_size_kb} KB")
    print(f"🗜️  Compression: {'Enabled' if compress_chunks else 'Disabled'}")
    if compress_chunks:
        print(f"🎨 Image quality: {compression_quality}%")
    
    # Process files
    start_time = datetime.now()
    all_chunks_info = process_pdf_files(
        pdf_files, files_dir, chunks_dir, max_size_kb, compress_chunks, compression_quality
    )
    end_time = datetime.now()
    
    # Generate report
    print(f"\n📊 Generating report...")
    report_path = generate_report(all_chunks_info, chunks_dir, max_size_kb, start_time, end_time, compress_chunks)
    
    # Final summary
    total_chunks = sum(len(info['chunks']) for info in all_chunks_info.values())
    successful_files = sum(1 for info in all_chunks_info.values() if info['chunks'])
    
    print(f"\n🎉 Processing Complete!")
    print(f"✅ Successfully processed: {successful_files}/{len(pdf_files)} files")
    print(f"📦 Total chunks created: {total_chunks}")
    print(f"⏱️  Total time: {(end_time - start_time).total_seconds():.2f} seconds")
    print(f"📄 Report saved: {report_path}")

if __name__ == "__main__":
    main() 