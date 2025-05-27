# Chonkie PDF

A powerful Python cli tool for splitting large PDF files into smaller chunks with advanced compression capabilities to handle problematic PDFs where individual pages retain the size of the entire document.

## 🚀 Features

- **Smart PDF Chunking**: Split PDFs by page count while respecting size limits
- **Advanced Compression**: Multiple compression libraries for optimal results
- **Automatic Problem Detection**: Identifies PDFs with oversized pages
- **Flexible Compression Options**: Choose compression quality and methods
- **Detailed Reporting**: Comprehensive reports with compression statistics
- **Fallback Support**: Works even without optional compression libraries

## 🔧 Compression Libraries

The tool supports multiple compression libraries in order of preference:

1. **pikepdf** (Recommended) - Advanced compression with:
   - Lossless content stream compression
   - Image quality optimization
   - Object deduplication
   - Orphaned object removal

2. **pypdf** - Modern compression with:
   - Content stream compression
   - Object deduplication
   - Efficient PDF optimization

3. **PyPDF2** (Fallback) - Basic compression:
   - Always available
   - Basic content stream compression

## 📦 Installation


### From requirements.txt
```bash
pip install -r requirements.txt
```

## 🎯 Usage

1. **Place your PDF files** in the `files/` directory
2. **Run the tool**:
   ```bash
   python main.py
   ```
3. **Follow the prompts**:
   - Enter maximum chunk size (e.g., 1024 KB)
   - Choose whether to enable compression (Y/n)
   - Set image compression quality (1-100, default 60)

## 📁 Directory Structure

```
├── files/                  # Place your PDF files here
├── chunks/                 # Generated chunks will be saved here
│   ├── filename1/         # Chunks for filename1.pdf
│   ├── filename2/         # Chunks for filename2.pdf
│   └── chunking_report.txt # Detailed processing report
|---utils                   # Utility functions
├── main.py                # Main application
├── requirements.txt       # Dependencies
```

## 🔍 How It Works

### Problem Detection
The tool automatically detects problematic PDFs where:
- Individual pages are unusually large (>80% of target chunk size)
- Pages retain the size of the entire document
- Embedded objects cause size inflation

### Compression Strategy
1. **Pre-analysis**: Check if original PDF needs compression
2. **Original Compression**: Compress the source PDF if beneficial
3. **Chunk-level Compression**: Compress individual chunks if they're still large
4. **Quality Control**: Only keep compressed versions if they provide >5% size reduction

### Compression Techniques
- **Content Stream Compression**: Lossless compression of PDF content
- **Image Optimization**: Reduce image quality while maintaining readability
- **Object Deduplication**: Remove duplicate objects and references
- **Orphaned Object Removal**: Clean up unused PDF objects

## 📊 Output

### Chunks
- Individual PDF files split by pages
- Automatically compressed if beneficial
- Named with clear numbering: `filename-1.pdf`, `filename-2.pdf`, etc.

### Report
Detailed `chunking_report.txt` includes:
- Processing statistics
- Compression ratios
- Available compression methods
- Per-file breakdown
- Oversized chunk warnings

## ⚙️ Configuration Options

### Compression Quality
- **1-30**: High compression, lower quality (good for text-heavy documents)
- **31-70**: Balanced compression and quality (recommended)
- **71-100**: Low compression, high quality (good for image-heavy documents)

### Size Thresholds
- **Compression Trigger**: Pages >80% of max size get compressed
- **Minimum Benefit**: Compression must provide >5% size reduction
- **Oversized Warning**: Pages exceeding max size are flagged

## 🛠️ Troubleshooting

### Common Issues

**"No compression libraries available"**
```bash
pip install pikepdf pypdf
```

**"Single page too large even after compression"**
- Try lower compression quality (20-40)
- Increase maximum chunk size
- Check if PDF contains high-resolution images

**"Compression not helping"**
- Some PDFs are already optimized
- Text-only PDFs may not compress much
- Try different compression libraries

### Performance Tips
- **pikepdf** is fastest for image-heavy PDFs
- **pypdf** is good for mixed content
- Lower compression quality = faster processing
- Larger chunk sizes = fewer files but potentially larger individual chunks

## 📈 Example Output

```
🚀 PDF Chunking Tool with Compression Started
============================================================

🔧 Available Compression Libraries:
   ✅ pikepdf (Advanced compression with image optimization)
   ✅ pypdf (Modern compression with object deduplication)
   ✅ PyPDF2 (Basic compression - always available)

📏 Enter maximum chunk size in KB (e.g., 1024): 1024
🗜️  Enable PDF compression? (Y/n): Y
🎨 Image compression quality (1-100, default 60): 60

🔍 Found 2 PDF files to process
📊 Maximum chunk size: 1024.0 KB
🗜️  Compression: Enabled
🎨 Image quality: 60%

📋 Progress: 1/2

📄 Processing: large_document.pdf
   Original size: 15234.56 KB
   Total pages: 45
   ⚠️  Single page size (14892.34 KB) is large, will attempt compression
   🗜️  Attempting to compress original PDF...
      Compressing PDF: large_document.pdf (15234.56 KB)
      ✅ Compressed using pikepdf: 3456.78 KB (77.3% reduction)
   ✅ Using compressed version for chunking
   ✅ Chunk 1: 15 pages, 987.65 KB
   ✅ Chunk 2: 15 pages, 1023.45 KB
   ✅ Chunk 3: 15 pages, 945.68 KB
   🎉 Successfully created 3 chunks
```

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool!

## 📄 License

This project is open source. Feel free to use and modify as needed. 

## 👨‍💻 Author

**Your Name**
- GitHub: [@TriptoAfsin](https://github.com/TriptoAfsin)
- Email: AfsinTripto@gmail.com
- LinkedIn: [Afshin Nahian Tripto](https://www.linkedin.com/in/triptoafsin)

---

*Built with ❤️ By Afshin Nahian Tripto*