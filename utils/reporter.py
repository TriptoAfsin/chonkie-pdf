"""
Report generation utilities for PDF chunking
"""
import os
from .dependencies import get_available_compression_methods

def generate_report(all_chunks_info, chunks_dir, max_size_kb, start_time, end_time, compression_enabled=True):
    """Generate a detailed report of the chunking process"""
    report_path = os.path.join(chunks_dir, "chunking_report.txt")
    
    total_original_files = len(all_chunks_info)
    total_chunks = sum(len(info['chunks']) for info in all_chunks_info.values())
    total_original_size = sum(info['original_size'] for info in all_chunks_info.values())
    total_chunks_size = sum(
        sum(chunk['size_kb'] for chunk in info['chunks']) 
        for info in all_chunks_info.values()
    )
    
    with open(report_path, 'w', encoding='utf-8') as report:
        report.write("=" * 80 + "\n")
        report.write("                    PDF CHUNKING REPORT\n")
        report.write("=" * 80 + "\n\n")
        
        report.write(f"Processing Date: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Completion Date: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Processing Time: {(end_time - start_time).total_seconds():.2f} seconds\n")
        report.write(f"Maximum Chunk Size: {max_size_kb} KB\n")
        report.write(f"Compression Enabled: {'Yes' if compression_enabled else 'No'}\n")
        
        # Report available compression libraries
        compression_libs = get_available_compression_methods()
        report.write(f"Available Compression Methods: {', '.join(compression_libs)}\n\n")
        
        report.write("SUMMARY:\n")
        report.write("-" * 40 + "\n")
        report.write(f"Total Original Files: {total_original_files}\n")
        report.write(f"Total Chunks Created: {total_chunks}\n")
        report.write(f"Total Original Size: {total_original_size:.2f} KB\n")
        report.write(f"Total Chunks Size: {total_chunks_size:.2f} KB\n")
        report.write(f"Size Difference: {abs(total_original_size - total_chunks_size):.2f} KB\n\n")
        
        report.write("DETAILED BREAKDOWN:\n")
        report.write("=" * 80 + "\n\n")
        
        for filename, file_info in all_chunks_info.items():
            report.write(f"📄 FILE: {filename}\n")
            report.write(f"   Original Size: {file_info['original_size']:.2f} KB\n")
            report.write(f"   Total Pages: {file_info['total_pages']}\n")
            report.write(f"   Chunks Created: {len(file_info['chunks'])}\n")
            report.write(f"   Status: {file_info['status']}\n\n")
            
            if file_info['chunks']:
                report.write("   CHUNKS:\n")
                for chunk in file_info['chunks']:
                    pages_range = f"{min(chunk['pages'])}-{max(chunk['pages'])}" if len(chunk['pages']) > 1 else str(chunk['pages'][0])
                    report.write(f"   • {chunk['filename']}: {chunk['size_kb']:.2f} KB, "
                               f"Pages {pages_range} ({chunk['page_count']} pages)\n")
                report.write("\n")
            
            report.write("-" * 80 + "\n\n")
        
        # Files that exceeded size limit
        oversized_chunks = []
        for file_info in all_chunks_info.values():
            for chunk in file_info['chunks']:
                if chunk['size_kb'] > max_size_kb:
                    oversized_chunks.append((file_info['filename'], chunk))
        
        if oversized_chunks:
            report.write("⚠️  CHUNKS EXCEEDING SIZE LIMIT:\n")
            report.write("-" * 40 + "\n")
            for filename, chunk in oversized_chunks:
                report.write(f"• {filename} - {chunk['filename']}: {chunk['size_kb']:.2f} KB\n")
            report.write("\n")
    
    print(f"\n📊 Report generated: {report_path}")
    return report_path 