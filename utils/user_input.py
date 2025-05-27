"""
User input handling utilities
"""

def get_chunk_size():
    """Get maximum chunk size from user input"""
    while True:
        try:
            max_size_kb = float(input("\n📏 Enter maximum chunk size in KB (e.g., 1024): "))
            if max_size_kb <= 0:
                print("❌ Please enter a positive number")
                continue
            return max_size_kb
        except ValueError:
            print("❌ Please enter a valid number")

def get_compression_settings():
    """Get compression preferences from user"""
    # Get compression preferences
    compress_chunks = True
    compression_quality = 60
    
    while True:
        compress_input = input("\n🗜️  Enable PDF compression? (Y/n): ").strip().lower()
        if compress_input in ['', 'y', 'yes']:
            compress_chunks = True
            break
        elif compress_input in ['n', 'no']:
            compress_chunks = False
            break
        else:
            print("❌ Please enter Y or N")
    
    if compress_chunks:
        while True:
            try:
                quality_input = input("\n🎨 Image compression quality (1-100, default 60): ").strip()
                if quality_input == '':
                    compression_quality = 60
                    break
                compression_quality = int(quality_input)
                if 1 <= compression_quality <= 100:
                    break
                else:
                    print("❌ Please enter a number between 1 and 100")
            except ValueError:
                print("❌ Please enter a valid number")
    
    return compress_chunks, compression_quality 