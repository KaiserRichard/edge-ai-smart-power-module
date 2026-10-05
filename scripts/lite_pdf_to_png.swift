// Rasterize native KiCad per-layer PDFs using macOS frameworks, without installs.
import Foundation
import CoreGraphics
import ImageIO

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(1)
}
if CommandLine.arguments.count != 3 { fail("Usage: fab_pdf_to_png.swift <pdfdir> <pngdir>") }
let source = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let target = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
let files = try FileManager.default.contentsOfDirectory(at: source, includingPropertiesForKeys: nil)
    .filter { $0.pathExtension.lowercased() == "pdf" }.sorted { $0.path < $1.path }
if files.isEmpty { fail("No layer PDFs to rasterize") }
let scale: CGFloat = 150.0 / 72.0
for file in files {
    guard let doc = CGPDFDocument(file as CFURL), doc.numberOfPages == 1,
          let page = doc.page(at: 1) else { fail("Expected a one-page layer PDF: \(file.path)") }
    let box = page.getBoxRect(.mediaBox)
    let width = Int(ceil(box.width * scale)), height = Int(ceil(box.height * scale))
    guard let ctx = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8,
        bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { fail("Cannot create bitmap") }
    ctx.setFillColor(CGColor(gray: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: width, height: height))
    ctx.scaleBy(x: scale, y: scale)
    ctx.translateBy(x: -box.minX, y: -box.minY)
    ctx.drawPDFPage(page)
    let output = target.appendingPathComponent(file.deletingPathExtension().lastPathComponent + ".png")
    guard let bitmap = ctx.makeImage(),
          let dest = CGImageDestinationCreateWithURL(output as CFURL, "public.png" as CFString, 1, nil)
          else { fail("Cannot create PNG \(output.path)") }
    CGImageDestinationAddImage(dest, bitmap, [kCGImagePropertyDPIWidth: 150,
        kCGImagePropertyDPIHeight: 150] as CFDictionary)
    if !CGImageDestinationFinalize(dest) { fail("Cannot write PNG \(output.path)") }
    print(output.lastPathComponent)
}
