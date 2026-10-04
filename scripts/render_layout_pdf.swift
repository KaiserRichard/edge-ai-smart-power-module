// Render native KiCad review PDFs with macOS PDFKit; no extra dependencies.
// swift render_layout_pdf.swift INPUT.pdf OUTPUT_PREFIX
import Foundation
import PDFKit
import AppKit

let args = CommandLine.arguments
guard args.count == 3,
      let document = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    fatalError("Usage: render_layout_pdf.swift INPUT.pdf OUTPUT_PREFIX")
}
for index in 0..<document.pageCount {
    let page = document.page(at: index)!
    let thumbnail = page.thumbnail(of: NSSize(width: 2200, height: 1800), for: .mediaBox)
    let bitmap = NSBitmapImageRep(data: thumbnail.tiffRepresentation!)!
    let data = bitmap.representation(using: .png, properties: [:])!
    try data.write(to: URL(fileURLWithPath: "\(args[2])_\(index + 1).png"))
}
print("Rendered \(document.pageCount) pages")
