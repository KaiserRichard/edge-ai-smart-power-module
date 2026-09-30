#import <Foundation/Foundation.h>
#import <PDFKit/PDFKit.h>
#import <AppKit/AppKit.h>
int main(int argc, const char * argv[]) { @autoreleasepool {
NSString *src = [NSString stringWithUTF8String:argv[1]];
NSString *out = [NSString stringWithUTF8String:argv[2]];
[[NSFileManager defaultManager] createDirectoryAtPath:out withIntermediateDirectories:YES attributes:nil error:nil];
PDFDocument *doc = [[PDFDocument alloc] initWithURL:[NSURL fileURLWithPath:src]];
NSMutableString *text = [NSMutableString string];
for (NSUInteger i=0; i<[doc pageCount]; i++) {
PDFPage *page = [doc pageAtIndex:i];
[text appendFormat:@"\n===== PDF PAGE %lu =====\n%@\n", i+1, [page string]];
NSRect box = [page boundsForBox:kPDFDisplayBoxMediaBox];
NSImage *im = [page thumbnailOfSize:NSMakeSize(2400,2400*box.size.height/box.size.width) forBox:kPDFDisplayBoxMediaBox];
NSBitmapImageRep *rep = [NSBitmapImageRep imageRepWithData:[im TIFFRepresentation]];
[[rep representationUsingType:NSBitmapImageFileTypePNG properties:@{}] writeToFile:[NSString stringWithFormat:@"%@/page-%lu.png",out,i+1] atomically:YES];
}
[text writeToFile:[out stringByAppendingPathComponent:@"pages.txt"] atomically:YES encoding:NSUTF8StringEncoding error:nil];
printf("Read %lu PDF pages\n",[doc pageCount]);
} return 0; }
