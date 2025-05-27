"""
PDF chunking functionality
"""
import os
import PyPDF2
from .file_utils import get_file_size_kb, create_chunk_directory
from .encryption import is_pdf_encrypted, handle_encrypted_pdf, check_encryption_support
from .compression import compress_pdf_file

def chunk_pdf_by_pages(pdf_path, max_size_kb, chunks_dir, compress_chunks=True, compression_quality=60):
    """
    Chunk a PDF file by pages to ensure each chunk is under max_size_kb
    Returns list of created chunk files and their info
    """
    print(f"\n📄 Processing: {os.path.basename(pdf_path)}")
    print(f"   Original size: {get_file_size_kb(pdf_path):.2f} KB")
    
    filename = os.path.basename(pdf_path)
    chunk_info = []
    
    # Check if PDF is encrypted
    if is_pdf_encrypted(pdf_path):
        print(f"   🔒 PDF is encrypted, attempting to decrypt...")
        if not check_encryption_support():
            print(f"   ❌ PyCryptodome is required for encrypted PDFs")
            print(f"   💡 Install with: pip install pycryptodome")
            return []
        
        # Try to handle encrypted PDF
        pdf_reader = handle_encrypted_pdf(pdf_path)
        if pdf_reader is None:
            return []
    
    # Check if we should compress the original file first
    should_compress_original = False
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Handle encryption if needed
            if pdf_reader.is_encrypted:
                if not check_encryption_support():
                    print(f"   ❌ PyCryptodome is required for encrypted PDFs")
                    print(f"   💡 Install with: pip install pycryptodome")
                    return []
                
                # Try to decrypt
                decrypted_reader = handle_encrypted_pdf(pdf_path)
                if decrypted_reader is None:
                    return []
                pdf_reader = decrypted_reader
            
            total_pages = len(pdf_reader.pages)
            
            # Check if single pages are problematically large
            if total_pages > 1:
                # Create a test single page to check its size
                test_writer = PyPDF2.PdfWriter()
                test_writer.add_page(pdf_reader.pages[0])
                
                test_path = os.path.join(chunks_dir, "temp_test_page.pdf")
                with open(test_path, 'wb') as test_file:
                    test_writer.write(test_file)
                
                single_page_size = get_file_size_kb(test_path)
                os.remove(test_path)
                
                # If a single page is more than 80% of max size, we should compress
                if single_page_size > (max_size_kb * 0.8):
                    should_compress_original = True
                    print(f"   ⚠️  Single page size ({single_page_size:.2f} KB) is large, will attempt compression")
    
    except Exception as e:
        print(f"   ❌ Error analyzing PDF: {e}")
        return []
    
    # Compress original if needed
    working_pdf_path = pdf_path
    if should_compress_original and compress_chunks:
        print(f"   🗜️  Attempting to compress original PDF...")
        compressed_path = os.path.join(chunks_dir, f"compressed_{filename}")
        success, compressed_path, ratio = compress_pdf_file(pdf_path, compressed_path, compression_quality)
        
        if success:
            working_pdf_path = compressed_path
            print(f"   ✅ Using compressed version for chunking")
        else:
            print(f"   📝 Using original file for chunking")
    
    try:
        with open(working_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"   Total pages: {total_pages}")
            
            # Create directory for this file's chunks
            file_chunk_dir = create_chunk_directory(chunks_dir, filename)
            
            current_chunk = PyPDF2.PdfWriter()
            current_chunk_pages = 0
            chunk_number = 1
            pages_in_current_chunk = []
            
            page_num = 0
            while page_num < total_pages:
                # Create a test chunk with the current page added
                test_chunk = PyPDF2.PdfWriter()
                
                # Add all existing pages to test chunk
                for existing_page_idx in range(current_chunk_pages):
                    start_page_num = page_num - current_chunk_pages
                    test_chunk.add_page(pdf_reader.pages[start_page_num + existing_page_idx])
                
                # Add the new page to test chunk
                test_chunk.add_page(pdf_reader.pages[page_num])
                
                # Create temporary file to check size
                temp_chunk_name = f"{filename.replace('.pdf', '')}-{chunk_number}.pdf"
                temp_chunk_path = os.path.join(file_chunk_dir, temp_chunk_name)
                
                with open(temp_chunk_path, 'wb') as temp_file:
                    test_chunk.write(temp_file)
                
                test_size = get_file_size_kb(temp_chunk_path)
                
                # If adding this page would exceed the limit
                if test_size > max_size_kb and current_chunk_pages > 0:
                    # Save the current chunk without this page
                    final_chunk = PyPDF2.PdfWriter()
                    for existing_page_idx in range(current_chunk_pages):
                        start_page_num = page_num - current_chunk_pages
                        final_chunk.add_page(pdf_reader.pages[start_page_num + existing_page_idx])
                    
                    with open(temp_chunk_path, 'wb') as chunk_file:
                        final_chunk.write(chunk_file)
                    
                    # Try to compress the chunk if it's still large
                    final_size = get_file_size_kb(temp_chunk_path)
                    if compress_chunks and final_size > max_size_kb * 0.8:
                        print(f"   🗜️  Compressing chunk {chunk_number}...")
                        compressed_chunk_path = temp_chunk_path.replace('.pdf', '_compressed.pdf')
                        success, final_path, ratio = compress_pdf_file(temp_chunk_path, compressed_chunk_path, compression_quality)
                        
                        if success:
                            os.remove(temp_chunk_path)  # Remove uncompressed version
                            temp_chunk_path = final_path
                            temp_chunk_name = os.path.basename(final_path)
                            final_size = get_file_size_kb(temp_chunk_path)
                    
                    chunk_info.append({
                        'chunk_number': chunk_number,
                        'filename': temp_chunk_name,
                        'path': temp_chunk_path,
                        'size_kb': final_size,
                        'pages': pages_in_current_chunk.copy(),
                        'page_count': current_chunk_pages
                    })
                    
                    print(f"   ✅ Chunk {chunk_number}: {current_chunk_pages} pages, {final_size:.2f} KB")
                    
                    # Start new chunk
                    chunk_number += 1
                    current_chunk_pages = 0
                    pages_in_current_chunk = []
                    # Don't increment page_num, we need to process this page in the new chunk
                    continue
                
                # If this is a single page and it exceeds the limit, we still need to save it
                elif test_size > max_size_kb and current_chunk_pages == 0:
                    print(f"   ⚠️  Warning: Page {page_num + 1} alone is {test_size:.2f} KB (exceeds limit)")
                    
                    # Try to compress this oversized single page
                    if compress_chunks:
                        print(f"   🗜️  Attempting to compress oversized page...")
                        compressed_chunk_path = temp_chunk_path.replace('.pdf', '_compressed.pdf')
                        success, final_path, ratio = compress_pdf_file(temp_chunk_path, compressed_chunk_path, compression_quality)
                        
                        if success:
                            os.remove(temp_chunk_path)  # Remove uncompressed version
                            temp_chunk_path = final_path
                            temp_chunk_name = os.path.basename(final_path)
                            test_size = get_file_size_kb(temp_chunk_path)
                    
                    # Save this oversized single page
                    chunk_info.append({
                        'chunk_number': chunk_number,
                        'filename': temp_chunk_name,
                        'path': temp_chunk_path,
                        'size_kb': test_size,
                        'pages': [page_num + 1],
                        'page_count': 1
                    })
                    
                    status = "compressed" if compress_chunks and test_size < max_size_kb else "oversized"
                    print(f"   ✅ Chunk {chunk_number}: 1 page, {test_size:.2f} KB ({status})")
                    
                    # Start new chunk
                    chunk_number += 1
                    current_chunk_pages = 0
                    pages_in_current_chunk = []
                    page_num += 1
                    continue
                
                # If we can add this page without exceeding the limit
                else:
                    current_chunk_pages += 1
                    pages_in_current_chunk.append(page_num + 1)
                    
                    # If this is the last page, save the chunk
                    if page_num == total_pages - 1:
                        # Try to compress the final chunk if it's large
                        if compress_chunks and test_size > max_size_kb * 0.8:
                            print(f"   🗜️  Compressing final chunk {chunk_number}...")
                            compressed_chunk_path = temp_chunk_path.replace('.pdf', '_compressed.pdf')
                            success, final_path, ratio = compress_pdf_file(temp_chunk_path, compressed_chunk_path, compression_quality)
                            
                            if success:
                                os.remove(temp_chunk_path)  # Remove uncompressed version
                                temp_chunk_path = final_path
                                temp_chunk_name = os.path.basename(final_path)
                                test_size = get_file_size_kb(temp_chunk_path)
                        
                        chunk_info.append({
                            'chunk_number': chunk_number,
                            'filename': temp_chunk_name,
                            'path': temp_chunk_path,
                            'size_kb': test_size,
                            'pages': pages_in_current_chunk.copy(),
                            'page_count': current_chunk_pages
                        })
                        
                        print(f"   ✅ Chunk {chunk_number}: {current_chunk_pages} pages, {test_size:.2f} KB")
                
                page_num += 1
            
            print(f"   🎉 Successfully created {len(chunk_info)} chunks")
            
            # Clean up compressed original if it was created
            if working_pdf_path != pdf_path and os.path.exists(working_pdf_path):
                os.remove(working_pdf_path)
            
            return chunk_info
            
    except Exception as e:
        print(f"   ❌ Error processing {filename}: {str(e)}")
        return [] 