// OCR helper for extract_erase_replies.py: reads text out of screenshots with
// macOS's built-in Vision framework, so no package has to be installed.
//
// Usage: ocr_screenshot <image.png> [<image.png> ...]
// Prints one JSON object per image (NDJSON) with each recognized line and its
// bounding box as fractions of the image (origin top-left, 0..1). Fractions,
// not pixels, because Copilot's screenshots are 4x the size of the others.
//
// Language correction is off on purpose: it "fixes" unusual words toward
// dictionary words, and every cell's token is a deliberately unusual codename.

import AppKit
import Foundation
import Vision

struct Line: Codable {
    let text: String
    let x: Double
    let y: Double
    let w: Double
    let h: Double
    let conf: Float
}

struct Result: Codable {
    let image: String
    let width: Int
    let height: Int
    let lines: [Line]
    let error: String?
}

func recognize(path: String) -> Result {
    guard let image = NSImage(contentsOfFile: path),
          let cg = image.cgImage(forProposedRect: nil, context: nil, hints: nil)
    else {
        return Result(image: path, width: 0, height: 0, lines: [], error: "cannot load image")
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    request.recognitionLanguages = ["en-US"]
    do {
        try VNImageRequestHandler(cgImage: cg, options: [:]).perform([request])
    } catch {
        return Result(image: path, width: cg.width, height: cg.height, lines: [], error: "\(error)")
    }
    let lines = (request.results ?? []).compactMap { observation -> Line? in
        guard let best = observation.topCandidates(1).first else { return nil }
        let box = observation.boundingBox  // Vision's origin is bottom-left
        return Line(
            text: best.string, x: box.minX, y: 1 - box.maxY,
            w: box.width, h: box.height, conf: best.confidence
        )
    }
    return Result(image: path, width: cg.width, height: cg.height, lines: lines, error: nil)
}

let encoder = JSONEncoder()
for path in CommandLine.arguments.dropFirst() {
    let data = try encoder.encode(recognize(path: path))
    print(String(decoding: data, as: UTF8.self))
    fflush(stdout)
}
