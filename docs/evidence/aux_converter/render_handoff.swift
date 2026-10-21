// Reproduce two original handout pages directly from AUX24_INTERFACE.md.
// macOS: swift docs/evidence/aux_converter/render_handoff.swift [--preview]
import Foundation
import CoreGraphics
import CoreText
import AppKit
import PDFKit

let directory = URL(fileURLWithPath: CommandLine.arguments[0]).deletingLastPathComponent()
let markdown = try String(contentsOf: directory.appendingPathComponent("AUX24_INTERFACE.md"), encoding: .utf8)
let output = directory.appendingPathComponent("OWNER_HANDOFF.pdf")
let width: CGFloat = 595.28, height: CGFloat = 841.89, margin: CGFloat = 38
let bodyWidth = width - 2 * margin
let ink = CGColor(red: 0.08, green: 0.13, blue: 0.21, alpha: 1)
let blue = CGColor(red: 0.10, green: 0.23, blue: 0.36, alpha: 1)
let pale = CGColor(red: 0.94, green: 0.96, blue: 0.98, alpha: 1)
let red = CGColor(red: 0.65, green: 0.14, blue: 0.12, alpha: 1)
var page = CGRect(x: 0, y: 0, width: width, height: height)
let metadata: [String: Any] = [kCGPDFContextTitle as String: "V1A auxiliary converter owner and buyer handoff", kCGPDFContextCreator as String: "Original engineering study; source AUX24_INTERFACE.md"]
guard let context = CGContext(output as CFURL, mediaBox: &page, metadata as CFDictionary) else { fatalError("Cannot create PDF") }

func clean(_ s: String) -> String {
    s.replacingOccurrences(of: "**", with: "").trimmingCharacters(in: .whitespacesAndNewlines)
}

func attributed(_ s: String, size: CGFloat, color: CGColor, bold: Bool = false) -> NSAttributedString {
    let font = CTFontCreateWithName((bold ? "Helvetica-Bold" : "Helvetica") as CFString, size, nil)
    return NSAttributedString(string: clean(s), attributes: [NSAttributedString.Key(kCTFontAttributeName as String): font, NSAttributedString.Key(kCTForegroundColorAttributeName as String): color])
}

func measured(_ s: String, size: CGFloat, availableWidth: CGFloat, bold: Bool = false) -> CGFloat {
    let value = attributed(s, size: size, color: ink, bold: bold)
    let setter = CTFramesetterCreateWithAttributedString(value)
    return ceil(CTFramesetterSuggestFrameSizeWithConstraints(setter, CFRange(location: 0, length: 0), nil, CGSize(width: availableWidth, height: 2000), nil).height) + 2
}

@discardableResult
func draw(_ s: String, x: CGFloat, top: CGFloat, availableWidth: CGFloat, size: CGFloat, color: CGColor = ink, bold: Bool = false) -> CGFloat {
    let value = attributed(s, size: size, color: color, bold: bold)
    let setter = CTFramesetterCreateWithAttributedString(value)
    let h = measured(s, size: size, availableWidth: availableWidth, bold: bold)
    let frame = CTFramesetterCreateFrame(setter, CFRange(location: 0, length: 0), CGPath(rect: CGRect(x: x, y: top - h, width: availableWidth, height: h), transform: nil), nil)
    let visible = CTFrameGetVisibleStringRange(frame)
    precondition(visible.length == value.length, "Clipped text")
    context.textMatrix = .identity
    CTFrameDraw(frame, context)
    return top - h
}

func startPage(_ title: String, number: Int) -> CGFloat {
    context.beginPDFPage(nil)
    var y = height - margin
    y = draw(title, x: margin, top: y, availableWidth: bodyWidth, size: 18, color: blue, bold: true) - 6
    y = draw("V1A upstream converter | 13S battery / PDB | 2026-09-30", x: margin, top: y, availableWidth: bodyWidth, size: 9) - 17
    context.setStrokeColor(blue); context.setLineWidth(1)
    context.move(to: CGPoint(x: margin, y: y + 8)); context.addLine(to: CGPoint(x: width - margin, y: y + 8)); context.strokePath()
    draw("STUDY ONLY - ENGINEERING REVIEW REQUIRED - NONE MEETS SPEC", x: margin, top: 32, availableWidth: bodyWidth - 20, size: 8, color: red, bold: true)
    draw("\(number)", x: width - margin - 15, top: 32, availableWidth: 15, size: 8)
    return y
}

func section(from start: String, until end: String) -> String {
    let a = markdown.range(of: start)!.upperBound
    let b = markdown.range(of: end, range: a..<markdown.endIndex)!.lowerBound
    return String(markdown[a..<b]).trimmingCharacters(in: .whitespacesAndNewlines)
}

let owner = section(from: "## OWNER EXPLANATION — one-page handout", until: "## Buyer handoff")
var y = startPage("Owner explanation", number: 1)
for paragraph in owner.components(separatedBy: "\n\n") {
    y = draw(paragraph, x: margin, top: y, availableWidth: bodyWidth, size: 11) - 10
}
precondition(y >= 55, "Owner explanation exceeds one page")
context.endPDFPage()

let buyer = section(from: "## Buyer handoff — proposed one-page interface specification", until: "### Power scenarios")
let lines = buyer.components(separatedBy: "\n")
let intro = lines.filter { !$0.hasPrefix("|") && !$0.isEmpty && !$0.hasPrefix("**CALCULATED:") }.joined(separator: " ")
let note = lines.first { $0.hasPrefix("**CALCULATED:") }!
let rows = lines.filter { $0.hasPrefix("|") && !$0.hasPrefix("|---") }.map {
    $0.split(separator: "|", omittingEmptySubsequences: true).map { clean(String($0)) }
}
precondition(rows.count == 11 && rows.allSatisfy { $0.count == 3 }, "Expected header plus S1-S10")
y = startPage("Buyer interface specification", number: 2)
y = draw(intro, x: margin, top: y, availableWidth: bodyWidth, size: 9.5) - 10
let columns: [CGFloat] = [76, 288, bodyWidth - 364]
for (index, row) in rows.enumerated() {
    let size: CGFloat = index == 0 ? 9 : 8.7
    let rowHeight = zip(row, columns).map { measured($0.0, size: size, availableWidth: $0.1 - 10, bold: index == 0) }.max()! + 10
    context.setFillColor(index == 0 ? blue : (index % 2 == 1 ? pale : CGColor(gray: 1, alpha: 1)))
    context.fill(CGRect(x: margin, y: y - rowHeight, width: bodyWidth, height: rowHeight))
    var x = margin
    for i in 0..<3 {
        draw(row[i], x: x + 5, top: y - 5, availableWidth: columns[i] - 10, size: size, color: index == 0 ? CGColor(gray: 1, alpha: 1) : ink, bold: index == 0 || i == 0)
        x += columns[i]
    }
    y -= rowHeight
}
y = draw(note, x: margin, top: y - 12, availableWidth: bodyWidth, size: 9) - 6
precondition(y >= 55, "Buyer specification exceeds one page")
context.endPDFPage(); context.closePDF()
let pdf = PDFDocument(url: output)!
precondition(pdf.pageCount == 2, "Expected exactly two pages")
print("Wrote \(output.path): 2 pages, all text fits; final buyer text bottom \(Int(y)) pt.")
if CommandLine.arguments.contains("--preview") {
    for i in 0..<pdf.pageCount {
        let thumb = pdf.page(at: i)!.thumbnail(of: NSSize(width: 900, height: 1273), for: .mediaBox)
        let rep = NSBitmapImageRep(data: thumb.tiffRepresentation!)!
        let path = directory.appendingPathComponent(".handoff-preview-\(i + 1).png")
        try rep.representation(using: .png, properties: [:])!.write(to: path)
    }
}
