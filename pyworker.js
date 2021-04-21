self.languagePluginUrl = "https://cdn.jsdelivr.net/pyodide/v0.16.1/full/";
importScripts("https://cdn.jsdelivr.net/pyodide/v0.16.1/full/pyodide.js");

class ChunkedFile {
  constructor(size) {
    this.data = [];
    this.offset = 0;
    this.size = size;
    this.buffer = new Uint8Array(new ArrayBuffer(size));
  }
  tell() {
    return this.offset;
  }
  read(size) {
    if (size === undefined) {
      size = this.size - this.offset;
    }
    if (this.offset >= this.size) {
      return null;
    }
    const readOffset = this.offset;
    this.offset += size;
    return this.buffer.slice(readOffset, readOffset + size);
  }
  seek(offset, whence) {
    switch (whence) {
      case 0:
        this.offset = offset;
        break;
      case 1:
        this.offset += offset;
        break;
      case 2:
        this.offset = this.size + offset;
        break;
    }
  }
  writeChunk(chunk) {
    this.buffer.set(chunk, this.offset);
    this.offset = this.offset + chunk.length;
  }
}

var data = undefined;

languagePluginLoader
  .then(() => {
    return pyodide.loadPackage("micropip");
  })
  .then(() => {
    return self.pyodide.runPython(
      `
import micropip
micropip.install(
    "http://localhost:8000/data_extractor/dist/data_extractor-0.1.0-py3-none-any.whl"
    )`
    );
  })
  .then(() => {
    self.pyodide.runPython(`
import data_extractor

class _ChunkedFile:
  def __init__(self, proxy):
    self.proxy = proxy

  def seekable(self):
    return True

  def seek(self, offset, whence=0):
    self.proxy.seek(offset, whence)

  def tell(self):
    return self.proxy.tell()

  def read(self, size=None):
    data = self.proxy.read(size)
    if data:
      return data.tobytes()


def _process_data(data):
  file_data = _ChunkedFile(data)
  return google_semantic_history_location.process(file_data)
  `);
    self.postMessage({ eventType: "initialized" });
  });

onmessage = (event) => {
  //await languagePluginLoader;
  //await pythonLoading;
  // Don't bother yet with this line, suppose our API is built in such a way:
  const { eventType } = event.data;
  if (eventType === "initData") {
    data = new ChunkedFile(event.data.size);
  } else if (eventType === "data") {
    data.writeChunk(event.data.chunk);
  } else if (eventType === "runPy") {
    const result = self.pyodide.globals._process_data(data);
    self.postMessage({ eventType: "result", result });
  }
};
