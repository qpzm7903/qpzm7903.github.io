// 生成站点默认 OG 分享图（1200×630）。
//
// 为什么用脚本而不是手工图片：OG 图是站点元数据的一部分，改标题/配色应当可复现、可评审。
// 依赖：macOS + CoreGraphics/CoreText（无第三方库）。
//
// 用法：swift scripts/gen-og-image.swift static/images/og-default.png
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let outPath = CommandLine.arguments.count > 1 ? CommandLine.arguments[1] : "static/images/og-default.png"
let W: CGFloat = 1200, H: CGFloat = 630

let cs = CGColorSpaceCreateDeviceRGB()
guard let ctx = CGContext(data: nil, width: Int(W), height: Int(H), bitsPerComponent: 8,
                          bytesPerRow: 0, space: cs,
                          bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else {
    FileHandle.standardError.write("无法创建绘图上下文\n".data(using: .utf8)!)
    exit(1)
}

func color(_ r: CGFloat, _ g: CGFloat, _ b: CGFloat, _ a: CGFloat = 1) -> CGColor {
    CGColor(colorSpace: cs, components: [r/255, g/255, b/255, a])!
}

// 背景：深蓝渐变（顶浅底深），叠加一点噪点感的横线
let grad = CGGradient(colorsSpace: cs,
                      colors: [color(23, 32, 56), color(10, 15, 28)] as CFArray,
                      locations: [0, 1])!
ctx.drawLinearGradient(grad, start: CGPoint(x: 0, y: H), end: CGPoint(x: W, y: 0), options: [])
ctx.setFillColor(color(37, 99, 235, 0.85))               // 品牌蓝强调条
ctx.fill(CGRect(x: 0, y: 0, width: W, height: 10))

// 文本绘制：CoreText，左上角为原点换算
func draw(_ text: String, font: String, size: CGFloat, x: CGFloat, y: CGFloat,
          color c: CGColor, maxWidth: CGFloat? = nil, lineSpacing: CGFloat = 8) {
    let f = CTFontCreateWithName(font as CFString, size, nil)
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(rawValue: kCTFontAttributeName as String): f,
        NSAttributedString.Key(rawValue: kCTForegroundColorAttributeName as String): c,
    ]
    let attr = NSAttributedString(string: text, attributes: attrs)
    let framesetter = CTFramesetterCreateWithAttributedString(attr)
    let constraints = CGSize(width: maxWidth ?? W, height: .greatestFiniteMagnitude)
    let suggested = CTFramesetterSuggestFrameSizeWithConstraints(framesetter, CFRange(location: 0, length: 0),
                                                                nil, constraints, nil)
    let rect = CGRect(x: x, y: y - suggested.height, width: maxWidth ?? suggested.width, height: suggested.height + 4)
    let path = CGPath(rect: rect, transform: nil)
    let frame = CTFramesetterCreateFrame(framesetter, CFRange(location: 0, length: 0), path, nil)
    CTFrameDraw(frame, ctx)
}

// 主标题
draw("科技热点日报", font: "PingFangSC-Semibold", size: 84, x: 90, y: H - 190, color: color(255, 255, 255))
// 副标题
draw("AI 前沿 · 技术深度 · 每日科技热点", font: "PingFangSC-Regular", size: 38, x: 92, y: H - 300,
     color: color(148, 163, 184))
// 分隔线
ctx.setStrokeColor(color(37, 99, 235, 0.55))
ctx.setLineWidth(3)
ctx.move(to: CGPoint(x: 92, y: H - 340)); ctx.addLine(to: CGPoint(x: W - 92, y: H - 340)); ctx.strokePath()
// 站点地址
draw("qpzm7903.github.io", font: "HelveticaNeue-Medium", size: 30, x: 92, y: 110, color: color(96, 165, 250))

guard let image = ctx.makeImage() else { exit(1) }
let url = URL(fileURLWithPath: outPath)
try? FileManager.default.createDirectory(at: url.deletingLastPathComponent(), withIntermediateDirectories: true)
// 输出 JPEG：渐变背景用 PNG 会有 ~680KB，不适合做 OG 图；JPEG 质量 0.85 约 60KB
let isJPEG = url.pathExtension.lowercased() == "jpg" || url.pathExtension.lowercased() == "jpeg"
let type = isJPEG ? UTType.jpeg.identifier : UTType.png.identifier
guard let dest = CGImageDestinationCreateWithURL(url as CFURL, type as CFString, 1, nil) else {
    exit(1)
}
CGImageDestinationAddImage(dest, image,
    [kCGImageDestinationLossyCompressionQuality: 0.85] as CFDictionary)
if CGImageDestinationFinalize(dest) {
    print("已生成 \(outPath) (\(Int(W))x\(Int(H)))")
} else {
    exit(1)
}
