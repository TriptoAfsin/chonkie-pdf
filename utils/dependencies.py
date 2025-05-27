"""
Dependency management for PDF processing libraries
"""

# PDF Compression libraries
try:
    import pikepdf
    PIKEPDF_AVAILABLE = True
except ImportError:
    PIKEPDF_AVAILABLE = False

try:
    from pypdf import PdfWriter, PdfReader
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import Crypto
    PYCRYPTODOME_AVAILABLE = True
except ImportError:
    PYCRYPTODOME_AVAILABLE = False

def print_dependency_status():
    """Print the status of all dependencies"""
    print("\n🔧 Available Compression Libraries:")
    if PIKEPDF_AVAILABLE:
        print("   ✅ pikepdf (Advanced compression with image optimization)")
    else:
        print("   ❌ pikepdf (Not installed - run: pip install pikepdf)")
    
    if PYPDF_AVAILABLE:
        print("   ✅ pypdf (Modern compression with object deduplication)")
    else:
        print("   ❌ pypdf (Not installed - run: pip install pypdf)")
    
    print("   ✅ PyPDF2 (Basic compression - always available)")
    
    print("\n🔐 Encryption Support:")
    if PYCRYPTODOME_AVAILABLE:
        print("   ✅ PyCryptodome (Can handle encrypted PDFs)")
    else:
        print("   ❌ PyCryptodome (Not installed - run: pip install pycryptodome)")
        print("   ⚠️  Encrypted PDFs will be skipped without this library")

def get_available_compression_methods():
    """Get list of available compression methods in order of preference"""
    methods = []
    
    if PIKEPDF_AVAILABLE:
        methods.append("pikepdf")
    
    if PYPDF_AVAILABLE:
        methods.append("pypdf")
    
    methods.append("PyPDF2 (basic)")
    
    return methods 