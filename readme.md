# StoneX — Stone Family Classifier

AI-powered stone slab classification using **DINOv2-small** visual encoder + **LAB color descriptor** fusion.

## 🚀 Quick Start

### Prerequisites
```bash
pip install streamlit torch torchvision timm opencv-python pillow albumentations numpy
```

### Required Files
Place these in the same directory as `app.py`:
- **`best_stone_model.pt`** — trained model checkpoint
- **`splits.pkl`** — family names and metadata

### Run the App
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

---

## 📋 Features

✅ **Multi-image upload** — process one or more images at once  
✅ **Top-5 predictions** — stone family names displayed in rank order  
✅ **No confidence scores** — clean, focused output  
✅ **GPU support** — auto-detects CUDA if available  
✅ **LAB color extraction** — 102-dim color descriptor per image  
✅ **DINOv2-small backbone** — fine-tuned vision transformer  

---

## 🏗️ Model Architecture

```
Image (224×224)
    ↓
[DINOv2-small backbone]
    ↓
[Visual Projector: 256-dim]  +  [LAB Color Branch: 102-dim]
    ↓                              ↓
[Fused Embedding: 358-dim]
    ↓
[Classifier: 309 stone families]
```

### What's Inside

| Component | Details |
|-----------|---------|
| **Visual Encoder** | DINOv2-small (frozen during Stage-1, fine-tuned in Stage-2) |
| **Color Branch** | 102-dim LAB descriptor (L mean/std, A mean/std, B mean/std, 16-bin histograms, 4×4 spatial grid) |
| **Embedding** | 358-dim fused vector (256 visual + 102 color), L2-normalized |
| **Classification** | Linear layer on fused embedding |

---

## 📸 Input Requirements

- **Format:** JPG, JPEG, or PNG
- **Size:** Any size (will be resized to 224×224)
- **Content:** Stone slab photos (best results with clear, well-lit images)

---

## 📤 Output Format

For each uploaded image, the app displays:

```
📸 [Original Image]

Top 5 Predicted Stone Families
1. Family Name A
2. Family Name B
3. Family Name C
4. Family Name D
5. Family Name E
```

**No confidence scores shown** — just ranked family names.

---

## ⚙️ Configuration

Edit these in `app.py` to customize:

```python
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # GPU/CPU
IMG_SIZE = 224  # Input image size
LAB_RAW_DIM = 102  # LAB descriptor dimension
```

---

## 🔧 Troubleshooting

### Model files not found
```
❌ Model files not found!
Expected: best_stone_model.pt, splits.pkl
```
→ Ensure both files are in the same directory as `app.py`

### Out of Memory
→ Run on CPU instead: comment out the CUDA check  
→ Reduce `IMG_SIZE` (though 224 is standard)

### Slow inference
→ Make sure GPU is being used: check `DEVICE` output  
→ For CPU inference, expect ~2-5s per image

---

## 📊 Dataset Context

The model was trained on:
- **309 stone families**
- **~43,000 deduplicated images**
- **80/20 train/val split**
- **Multi-stage training:** Stage-1 (partial unfreeze) → Stage-2 (full unfreeze)

---

## 💡 How It Works

1. **Upload image** → Convert to RGB, resize to 224×224
2. **Extract LAB color** → 102-dim descriptor (color statistics + spatial distribution)
3. **Visual embedding** → DINOv2 backbone → 256-dim visual vector
4. **Fuse** → Concatenate visual (256) + color (102) = 358-dim
5. **Classify** → Linear classifier on fused embedding
6. **Rank** → Return top-5 families (sorted by logit scores)

---

## 📝 Training Notes

The model uses:
- **Loss:** 0.5·SupCon(fused) + 0.2·CrossEntropy + 0.3·SupCon(color)
- **Optimizer:** AdamW with 3 parameter groups (different LRs for backbone/projectors)
- **Scheduler:** CosineAnnealingWarmRestarts
- **Validation Metrics:** Recall@1 ~97%, Recall@5 ~99%

---

## 🎯 Next Steps

- Deploy with Docker or Streamlit Cloud
- Add FAISS index for similarity search
- Fine-tune on your custom stone dataset
- Export ONNX model for inference optimization

---

**v2.0** — DINOv2 + LAB Color Fusion  
Built with Streamlit + PyTorch