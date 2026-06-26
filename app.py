import streamlit as st
import torch
import torch.nn as nn
import torch.nn.functional as F
import cv2
import numpy as np
import pickle
from pathlib import Path
import timm
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from cmd_maapping import resolve_family_name

# ============================================================================
# CONFIG
# ============================================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMG_SIZE = 224
LAB_RAW_DIM = 102

# Transforms (same as training)
VAL_TF = A.Compose([
    A.Resize(IMG_SIZE, IMG_SIZE),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

# ============================================================================
# LAB COLOR FEATURE EXTRACTION
# ============================================================================

def extract_lab_features(img_bgr, target_size=112):
    """
    Extract 102-dim CIE-LAB color descriptor from BGR image.
    - 6 global stats (L/A/B mean + std)
    - 48 histogram values (16-bin × 3 channels)
    - 48 spatial grid means (4×4 grid × 3 channels)
    """
    if img_bgr is None:
        return np.zeros(LAB_RAW_DIM, dtype=np.float32)

    img = cv2.resize(img_bgr, (target_size, target_size), interpolation=cv2.INTER_AREA)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab).astype(np.float32)

    # Normalize to [0, 1]
    lab[:, :, 0] /= 100.0
    lab[:, :, 1] = (lab[:, :, 1] + 128) / 255.0
    lab[:, :, 2] = (lab[:, :, 2] + 128) / 255.0

    # Global mean + std (6)
    mean = lab.mean(axis=(0, 1))
    std = lab.std(axis=(0, 1))

    # 16-bin histograms per channel (48)
    hists = []
    for c in range(3):
        h, _ = np.histogram(lab[:, :, c], bins=16, range=(0, 1))
        h = h.astype(np.float32) / (h.sum() + 1e-6)
        hists.append(h)
    hists = np.concatenate(hists)

    # 4×4 spatial grid LAB means (48)
    GS = target_size // 4
    spatial = []
    for i in range(4):
        for j in range(4):
            patch = lab[i*GS:(i+1)*GS, j*GS:(j+1)*GS]
            spatial.append(patch.mean(axis=(0, 1)))
    spatial = np.concatenate(spatial)

    feat = np.concatenate([mean, std, hists, spatial]).astype(np.float32)
    return feat


# ============================================================================
# MODEL ARCHITECTURE
# ============================================================================

class StoneEmbedder(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        # Visual backbone (DINOv2-small)
        self.backbone = timm.create_model(
            'vit_small_patch14_dinov2.lvd142m',
            pretrained=True, num_classes=0, img_size=IMG_SIZE,
        )
        bdim = self.backbone.num_features
        for p in self.backbone.parameters():
            p.requires_grad = False

        # Visual projector: backbone_dim → 256
        PROJ_DIM = 512
        EMBED_DIM = 256
        self.visual_proj = nn.Sequential(
            nn.Linear(bdim, PROJ_DIM), nn.LayerNorm(PROJ_DIM),
            nn.GELU(), nn.Dropout(0.1),
            nn.Linear(PROJ_DIM, EMBED_DIM),
        )

        # Color branch (LAB MLP)
        LAB_PROJ = 102
        self.color_proj = nn.Sequential(
            nn.Linear(LAB_RAW_DIM, 192), nn.LayerNorm(192),
            nn.GELU(), nn.Dropout(0.1),
            nn.Linear(192, LAB_PROJ),
        )

        # Fused classifier
        FUSED_DIM = EMBED_DIM + LAB_PROJ  # 256 + 102 = 358
        self.classifier = nn.Linear(FUSED_DIM, num_classes)

    def forward(self, x, lab_vec=None, return_embedding=False):
        """
        x: (B, 3, H, W) image tensor
        lab_vec: (B, 102) LAB descriptor
        return_embedding: if True, return only fused embedding
        """
        feat = self.backbone(x)
        vis_emb = F.normalize(self.visual_proj(feat), dim=-1)  # (B, 256)

        if lab_vec is not None:
            col_emb = F.normalize(self.color_proj(lab_vec), dim=-1)  # (B, 102)
            fused = F.normalize(torch.cat([vis_emb, col_emb], dim=-1), dim=-1)
        else:
            zeros = torch.zeros(vis_emb.size(0), 102, device=vis_emb.device)
            fused = F.normalize(torch.cat([vis_emb, zeros], dim=-1), dim=-1)
            col_emb = zeros

        if return_embedding:
            return fused

        logits = self.classifier(fused)
        return fused, logits, vis_emb, col_emb


# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(page_title="StoneX — Stone Family Classifier", layout="wide")

st.markdown("""
# 🪨 StoneX — AI Stone Family Classifier
**DINOv2 + LAB Color Fusion**

Upload one or more stone slab images to get top-5 predicted stone family names.
""")

# ============================================================================
# LOAD MODEL & METADATA
# ============================================================================

@st.cache_resource
def load_model_and_metadata():
    """Load trained model and family metadata."""

    app_dir = Path(__file__).resolve().parent
    model_path = app_dir / "best_stone_model.pt"
    splits_path = app_dir / "splits.pkl"
    
    if not model_path.exists() or not splits_path.exists():
        st.error(f"❌ Model files not found!")
        st.info(f"Expected files in current directory:")
        st.info(f"  - `best_stone_model.pt`\n  - `splits.pkl`")
        st.stop()
    
    # Load metadata
    with open(splits_path, 'rb') as f:
        splits = pickle.load(f)
    
    family_names = splits['FAMILY_NAMES']
    num_classes = len(family_names)
    
    # Load model
    model = StoneEmbedder(num_classes).to(DEVICE)
    ckpt = torch.load(model_path, map_location=DEVICE)
    model.load_state_dict(ckpt['model'])
    model.eval()
    
    # Freeze all parameters
    for p in model.parameters():
        p.requires_grad = False
    
    st.success(f"✅ Model loaded! {num_classes} stone families")
    
    return model, family_names


try:
    model, family_names = load_model_and_metadata()
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# ============================================================================
# IMAGE UPLOAD & PREDICTION
# ============================================================================

st.markdown("---")
st.subheader("📸 Upload Images")

uploaded_files = st.file_uploader(
    "Upload one or more stone slab images (JPG, PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    help="Upload stone slab photos for family classification"
)

if not uploaded_files:
    st.info("👆 Upload images to get started")
    st.stop()

st.markdown("---")
st.subheader("🔍 Predictions")

# Process each image
for file_idx, uploaded_file in enumerate(uploaded_files, 1):
    col1, col2 = st.columns([1, 2])
    
    # Load and display image
    try:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3 and img_array.shape[2] == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            st.warning(f"⚠️  Image {file_idx}: Invalid format")
            continue
        
        # Display image
        with col1:
            st.image(image, use_column_width=True, caption=f"Image {file_idx}: {uploaded_file.name}")
        
        # Extract LAB features
        lab_features = extract_lab_features(img_bgr)
        lab_tensor = torch.from_numpy(lab_features).unsqueeze(0).to(DEVICE)
        
        # Prepare image tensor
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_tensor = VAL_TF(image=img_rgb)['image'].unsqueeze(0).to(DEVICE)
        
        # Forward pass
        with torch.no_grad():
            _, logits, _, _ = model(img_tensor, lab_tensor)
        
        # Get top 5 predictions
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()
        top5_indices = np.argsort(probs)[::-1][:5]
        top5_predictions = [
            (resolve_family_name(family_names[idx]), probs[idx])
            for idx in top5_indices
        ]
        
        # Display results
        with col2:
            st.markdown(f"#### Top 5 Predicted Stone Families")
            for rank, (family, score) in enumerate(top5_predictions, 1):
                st.markdown(f"**{rank}. {family}** — Similarity score: `{score:.4f}`")
        
        st.markdown("")
    
    except Exception as e:
        st.error(f"❌ Error processing image {file_idx} ({uploaded_file.name}): {str(e)}")

st.markdown("---")
st.caption("StoneX v2.0 — DINOv2 Visual + LAB Color Descriptor Fusion")
