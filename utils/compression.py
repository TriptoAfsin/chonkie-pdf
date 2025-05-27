"""
PDF compression utilities using various libraries
"""
import os
import PyPDF2
from .dependencies import PIKEPDF_AVAILABLE, PYPDF_AVAILABLE
from .file_utils import get_file_size_kb

# Import libraries conditionally
if PIKEPDF_AVAILABLE:
    import pikepdf

if PYPDF_AVAILABLE:
    from pypdf import PdfWriter, PdfReader

def compress_pdf_pikepdf(input_path, output_path, quality=60):
    """
    Compress PDF using pikepdf library with advanced compression
    """
    if not PIKEPDF_AVAILABLE:
        return False
        
    try:
        with pikepdf.open(input_path) as pdf:
            # Apply various compression techniques
            
            # 1. Remove duplicate objects and orphaned objects
            pdf.remove_unreferenced_resources()
            
            # 2. Compress images if they exist
            for page in pdf.pages:
                try:
                    # Get page resources
                    if '/Resources' in page and '/XObject' in page['/Resources']:
                        xobjects = page['/Resources']['/XObject']
                        for name, obj in xobjects.items():
                            if hasattr(obj, 'Subtype') and obj.Subtype == '/Image':
                                try:
                                    # Try to compress image
                                    if hasattr(obj, 'as_pil_image'):
                                        pil_image = obj.as_pil_image()
                                        if pil_image.mode in ['RGB', 'RGBA', 'L']:
                                            # This is a simplified approach - actual image replacement is complex
                                            pass
                                except Exception as e:
                                    print(f"      Warning: Could not process image {name}: {e}")
                                    continue
                except Exception as e:
                    print(f"      Warning: Could not process images on page: {e}")
                    continue
            
            # Save compressed PDF with compression options
            pdf.save(output_path, 
                    compress_streams=True, 
                    object_stream_mode=pikepdf.ObjectStreamMode.generate,
                    normalize_content=True,
                    linearize=True)
            return True
            
    except Exception as e:
        print(f"      Error with pikepdf compression: {e}")
        return False

def compress_pdf_pypdf(input_path, output_path):
    """
    Compress PDF using pypdf library
    """
    if not PYPDF_AVAILABLE:
        return False
        
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Compress content streams after adding pages to writer
        for page in writer.pages:
            try:
                page.compress_content_streams()
            except Exception as e:
                print(f"      Warning: Could not compress content streams for page: {e}")
                continue
        
        # Remove duplicate objects
        try:
            writer.compress_identical_objects(remove_identicals=True, remove_orphans=True)
        except Exception as e:
            print(f"      Warning: Could not compress identical objects: {e}")
        
        # Write compressed PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
        
    except Exception as e:
        print(f"      Error with pypdf compression: {e}")
        return False

def compress_pdf_basic(input_path, output_path):
    """
    Basic compression using PyPDF2 (fallback method)
    """
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()
            
            # Copy all pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Try to compress content streams after adding pages
            for page in writer.pages:
                try:
                    if hasattr(page, 'compress_content_streams'):
                        page.compress_content_streams()
                except Exception as e:
                    print(f"      Warning: Could not compress page content: {e}")
                    continue
            
            # Write to output
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
        
        return True
        
    except Exception as e:
        print(f"      Error with basic compression: {e}")
        return False

def compress_pdf_file(input_path, output_path=None, quality=60):
    """
    Compress a PDF file using the best available method
    Returns: (success, output_path, compression_ratio)
    """
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}{ext}"
    
    original_size = get_file_size_kb(input_path)
    print(f"      Compressing PDF: {os.path.basename(input_path)} ({original_size:.2f} KB)")
    
    # Try compression methods in order of preference
    compression_methods = []
    
    if PIKEPDF_AVAILABLE:
        compression_methods.append(("pikepdf", lambda: compress_pdf_pikepdf(input_path, output_path, quality)))
    
    if PYPDF_AVAILABLE:
        compression_methods.append(("pypdf", lambda: compress_pdf_pypdf(input_path, output_path)))
    
    compression_methods.append(("basic", lambda: compress_pdf_basic(input_path, output_path)))
    
    for method_name, compress_func in compression_methods:
        try:
            if compress_func():
                compressed_size = get_file_size_kb(output_path)
                compression_ratio = (original_size - compressed_size) / original_size * 100
                
                print(f"      ✅ Compressed using {method_name}: {compressed_size:.2f} KB "
                      f"({compression_ratio:.1f}% reduction)")
                
                # If compression didn't help much, use original
                if compression_ratio < 5:  # Less than 5% reduction
                    print(f"      📝 Compression ratio too low, keeping original")
                    if os.path.exists(output_path):
                        os.remove(output_path)
                    return False, input_path, 0
                
                return True, output_path, compression_ratio
                
        except Exception as e:
            print(f"      ❌ {method_name} compression failed: {e}")
            continue
    
    print(f"      ❌ All compression methods failed")
    return False, input_path, 0 