/** clipWorker の main-thread 側ラッパー。シングルトンでモデルを保持する。 */

export interface LoadProgress {
  /** 0..100 (最大ファイルの進捗) */
  percent: number;
  file: string;
}

type Pending = {
  resolve: (v: Float32Array) => void;
  reject: (e: Error) => void;
};

class ClipEngine {
  private worker: Worker | null = null;
  private nextId = 1;
  private pending = new Map<number, Pending>();
  private readyPromise: Promise<string> | null = null;
  private progressListeners = new Set<(p: LoadProgress) => void>();

  onProgress(fn: (p: LoadProgress) => void): () => void {
    this.progressListeners.add(fn);
    return () => this.progressListeners.delete(fn);
  }

  /** モデルの読み込みを開始(冪等)。解決値は実行デバイス名。 */
  load(): Promise<string> {
    this.readyPromise ??= new Promise<string>((resolve, reject) => {
      const worker = new Worker(new URL("./clipWorker.ts", import.meta.url), {
        type: "module",
      });
      this.worker = worker;
      worker.onmessage = (e: MessageEvent) => {
        const msg = e.data;
        if (msg.type === "progress") {
          for (const fn of this.progressListeners) {
            fn({ percent: msg.progress ?? 0, file: msg.file ?? "" });
          }
        } else if (msg.type === "ready") {
          resolve(msg.device);
        } else if (msg.type === "embedding") {
          this.pending.get(msg.id)?.resolve(msg.vector);
          this.pending.delete(msg.id);
        } else if (msg.type === "error") {
          const err = new Error(msg.message);
          if (msg.id != null) {
            this.pending.get(msg.id)?.reject(err);
            this.pending.delete(msg.id);
          } else {
            reject(err);
          }
        }
      };
      worker.onerror = (e) => reject(new Error(e.message));
      worker.postMessage({ type: "load" });
    });
    return this.readyPromise;
  }

  async embed(image: ImageBitmap): Promise<Float32Array> {
    await this.load();
    const id = this.nextId++;
    return new Promise<Float32Array>((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.worker!.postMessage({ type: "embed", id, bitmap: image });
    });
  }
}

/** アプリ全体で 1 つ。ページを離れるまでモデルを保持する。 */
export const clipEngine = new ClipEngine();
