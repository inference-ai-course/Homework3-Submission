# 資料截取方法與語音助理架構 — 開發參考指南

> 整理自 Week 3 作業（Notebook 02–08）的實測數據與結論，供後續專案開發做技術選型依據。

---

## 目錄

1. [網頁文字截取](#1-網頁文字截取)
2. [OCR / 文件截取](#2-ocr--文件截取)
3. [語音辨識 ASR](#3-語音辨識-asr)
4. [文字轉語音 TTS](#4-文字轉語音-tts)
5. [語音助理架構評估](#5-語音助理架構評估)
6. [按專案類型的選型速查表](#6-按專案類型的選型速查表)

---

## 1. 網頁文字截取

### 工具比較

| 工具 | 輸出格式 | JS 支援 | Python | 實測（arXiv 頁面） | 適用場景 |
|------|---------|--------|--------|------------------|---------|
| **trafilatura** | 純文字 | ❌ | 3.7+ | 2,434 字 / 0.2s | 大量、靜態文章批次抽取 |
| **html2text** | Markdown | ❌ | 3.6+ | — | Python 3.9、靜態頁輕量備案 |
| **Crawl4AI** | Markdown | ✅（headless 瀏覽器）| 3.10+ | 8,714 字 / 3.2s | JS-heavy 網站、LLM pipeline |

### 關鍵結論

- **trafilatura：快但會漏內容。** 它假設頁面是「報紙文章」結構；遇到非文章型頁面（如 Meta blog）只抽到 120 字，且夾雜導覽列/頁尾雜訊（boilerplate leakage）。
- **Crawl4AI：內容多 ~3.5 倍、保留 Markdown 結構**（標題、連結、清單），但慢約 16 倍、需要瀏覽器渲染。
- **輸出格式的影響**：純文字夠用於只需主體內容的任務；但 Markdown 保留階層與格式，對摘要、QA、需理解文件結構的下游 LLM 任務有明顯幫助。

### 選型建議

- CommonCrawl 規模的批次清洗、結構簡單的文章 → **trafilatura**（速度優先）
- JS 動態網站、文件/論文、要餵給 LLM 的少量高品質資料 → **Crawl4AI**
- Python 3.9 受限環境的靜態頁 → **html2text**

---

## 2. OCR / 文件截取

### 工具比較

| 工具 | 推出 | 實測 | 重點特性 | 限制 |
|------|------|------|---------|------|
| **Tesseract** | 2006 | 324 字 / 0.2s | 免費、離線、零依賴 | 「版面盲」，把 "Llama 4" 誤判成 "a 4"；多欄/表格會錯亂 |
| **EasyOCR** | 2020 | 341 字 / 1.6s（信心 0.826）| PyTorch、80+ 語言、文字準確度較高 | 較慢、需較多資源 |
| **Marker** | 2025 | 2,447 字 / 75.8s | PDF→Markdown，**正確還原表格/公式/多欄** | 慢，需 GPU 才快 |
| **Docling** | 2025 | benchmark：CPU 3.1s/頁 | 企業級，支援 DOCX/PPTX/XLSX/HTML | 安裝依賴較多 |

### 關鍵結論

- **OCR 演進主軸：從「純文字抽取」→「版面感知（layout-aware）」。** Tesseract 把頁面當成一袋文字；Marker/Docling 能保留結構與元素間關係。
- **版面感知決定資料品質**：表格、多欄、公式、程式碼若被打亂，會降低 LLM 訓練資料的可用性，甚至反噬模型品質。
- 文字準確度：**EasyOCR > Tesseract**。結構化需求：**Marker / Docling**。

### 選型建議

- 乾淨單欄掃描件、無 GPU、需離線/air-gapped → **Tesseract**（並可作大語料的快速第一遍預篩）
- 多語言文件、場景文字 → **EasyOCR**
- 複雜 PDF（論文、表格、公式）轉 Markdown 餵 LLM → **Marker**（2026 推薦的「最安全預設」）
- 多格式（DOCX/PPTX/HTML）、需 CPU 高吞吐、整合 LangChain/LlamaIndex → **Docling**

---

## 3. 語音辨識 ASR

### 模型大小比較（Whisper / faster-whisper）

| Model | 參數 | 速度 | 定位 |
|-------|------|------|------|
| tiny | 39M | 最快 | 快速測試 |
| base | 74M | 快 | 良好預設、大量轉錄的速度/準確平衡 |
| small | 244M | 中 | 較高準確 |
| medium | 769M | 慢 | 高準確 |
| large-v3 | 1.5B | 最慢 | 最高準確 |
| **turbo** | 809M | 比 large 快 6x | **2025 最佳速度/準確平衡** |

### 關鍵結論

- **後端用 `faster-whisper`（CTranslate2）**：比原版 Whisper 快約 4 倍、記憶體更省；支援 INT8 量化（CPU 友善）、batched inference、word-level 時間戳。
- **音質決定成敗**：實測 base 在吵雜音檔上辨識崩潰（出現亂碼）。模型大小要對應音源品質。
- **ASR 文字需後處理**：標點還原、錯字修正後再進訓練語料。
- 大量轉錄（如 1000 小時 podcast）→ **base**（平衡）；對準確要求高 → **turbo / large-v3**。

### 倫理 / 合規提醒

- 即使是公開音訊，轉錄與使用仍需考量隱私、同意、版權與平台政策；ASR 錯誤可能造成誤述（misrepresentation）。

---

## 4. 文字轉語音 TTS

| 工具 | 類型 | 優點 | 限制 |
|------|------|------|------|
| **edge-tts** | 雲端、免費 | 自然、好上手（如 `en-US-AriaNeural`）| 需網路、長文有延遲、網路 round-trip 成為即時瓶頸 |
| **Kokoro** | 本地 | **低延遲且穩定**、品質高 | 需本地運算資源 |

**結論**：非即時 / 網路穩定 → edge-tts 即可；**即時語音助理 → Kokoro**（本地、延遲可控，維持自然對話節奏）。

---

## 5. 語音助理架構評估

### 兩種架構的心智模型

```
Manual FastAPI  =  請求 / 回應 (request → response)
Pipecat         =  串流 / 事件 (continuous stream / events)
```

### 對照表

| 面向 | Manual FastAPI | Pipecat |
|------|----------------|---------|
| 建置複雜度 | 高（全部自己寫） | 低（可組合 pipeline） |
| 即時串流 | 手動 WebSocket | 內建 WebRTC |
| 輪次偵測 (turn detection) | 手動 VAD | 自動 |
| 打斷處理 (interruption) | ❌ 不支援 | ✅ 內建 |
| 換服務 (ASR/LLM/TTS) | 改程式碼 | 改設定 |

### 實測延遲（檔案式 FastAPI 單輪）

```
ASR  2.60s  +  LLM 1.83s  +  TTS 0.82s  ≈  總計 5.25s
```

> 「等使用者講完整段 → 上傳 → 回完整音檔」的批次延遲，對真實對話太慢。

### 結論：生產/真實對話首選 **Pipecat**

1. 語音對話的核心體驗是**低延遲 + 可被打斷**，需要 streaming 架構；FastAPI 的 request/response 模型天生做不到自然打斷。
2. Pipecat 把 VAD、turn detection、interruption、WebRTC 都抽象掉，可專注 agent 邏輯；換 TTS 只要改設定。
3. **何時才用 Manual FastAPI**：學習理解原理、需求極簡的單輪問答、或需完全掌控每個元件。

### 推薦的生產管線

```
WebRTC 音訊
  → faster-whisper (turbo, streaming)
  → Claude (system prompt 限制 1–3 句、max_tokens 低 ≈150)
  → Kokoro (本地、streaming 輸出)
  ── 全部由 Pipecat 編排，支援打斷與多輪記憶
```

**延遲調校重點**
- LLM 回應要短：語音場景 `max_tokens≈150`，system prompt 明確要求「簡潔，1–3 句」。
- TTS 要邊產生邊播（streaming），把感知延遲壓到對話可接受範圍。
- 最大延遲瓶頸通常是 **LLM**（尤其大模型跑 CPU 時），其次是 ASR；TTS 用本地模型可壓很低。

---

## 6. 按專案類型的選型速查表

| 內容來源 | 推薦工具 | 理由 |
|---------|---------|------|
| 一般網頁文章（大量） | trafilatura | 快、boilerplate 移除佳 |
| JS 動態網站 / 文件站 | Crawl4AI | 渲染 JS、保留 Markdown 結構 |
| 複雜版面 PDF（論文/表格） | Marker | 版面感知、轉 Markdown |
| 多格式企業文件 | Docling | DOCX/PPTX/HTML、CPU 高吞吐 |
| 乾淨掃描件 / 離線環境 | Tesseract | 免費、離線、零依賴 |
| 多語言 / 場景文字 | EasyOCR | 80+ 語言、準確度較高 |
| 音訊（大量轉錄） | faster-whisper (base) | 速度/準確平衡 |
| 音訊（高準確需求） | faster-whisper (turbo/large-v3) | 最佳準確 |
| 即時語音輸出 | Kokoro (TTS) | 本地、低延遲 |
| 非即時語音輸出 | edge-tts | 免費、自然 |
| 即時語音助理（端到端） | Pipecat | streaming、打斷處理、可組合 |

---

## 資料清洗備忘（補充）

- **去重**：MinHash（datasketch）；門檻依需求調整 — 高精度容忍重複用 0.8–0.9，重視縮減容忍少量遺失用 0.6–0.7。
- **過濾**：語言過濾常是移除最多文件的階段（網路資料多語言）；注意混語文件的 false positive。
- **規模化**：10 → 100 億份文件需分散式框架（Spark/Dask）、Parquet 儲存、streaming 處理；參考 HuggingFace **DataTrove / FineWeb** 的多階段（精確+近似）去重與品質過濾。
- **PII 移除**：醫療（HIPAA）等領域為法規要求；音訊來源需先移除 disfluency（um/uh）。

---

*參考資料：trafilatura、Crawl4AI、Tesseract、EasyOCR、Marker、Docling、faster-whisper、Kokoro、edge-tts、Pipecat、DataTrove/FineWeb 官方文件。*
