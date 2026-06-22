import csv
import pickle
from pathlib import Path

import albumentations as A
import cv2
import numpy as np
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from albumentations.pytorch import ToTensorV2


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
IMG_SIZE = 224
LAB_RAW_DIM = 102
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "best_stone_model.pt"
SPLITS_PATH = ROOT / "splits.pkl"
OUTPUT_CSV = ROOT / "test_predictions.csv"

INPUT_DIRS = [
    Path("/home/Unthinkable/Downloads/All Test Images"),
    Path("/home/Unthinkable/Downloads/Test Images 2"),
]

VAL_TF = A.Compose(
    [
        A.Resize(IMG_SIZE, IMG_SIZE),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ]
)


def extract_lab_features(img_bgr, target_size=112):
    if img_bgr is None:
        return np.zeros(LAB_RAW_DIM, dtype=np.float32)

    img = cv2.resize(img_bgr, (target_size, target_size), interpolation=cv2.INTER_AREA)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2Lab).astype(np.float32)

    lab[:, :, 0] /= 100.0
    lab[:, :, 1] = (lab[:, :, 1] + 128) / 255.0
    lab[:, :, 2] = (lab[:, :, 2] + 128) / 255.0

    mean = lab.mean(axis=(0, 1))
    std = lab.std(axis=(0, 1))

    hists = []
    for c in range(3):
        h, _ = np.histogram(lab[:, :, c], bins=16, range=(0, 1))
        hists.append(h.astype(np.float32) / (h.sum() + 1e-6))

    gs = target_size // 4
    spatial = []
    for i in range(4):
        for j in range(4):
            patch = lab[i * gs : (i + 1) * gs, j * gs : (j + 1) * gs]
            spatial.append(patch.mean(axis=(0, 1)))

    return np.concatenate([mean, std, np.concatenate(hists), np.concatenate(spatial)]).astype(
        np.float32
    )


class StoneEmbedder(nn.Module):
    def __init__(self, num_classes):
        super().__init__()

        self.backbone = timm.create_model(
            "vit_small_patch14_dinov2.lvd142m",
            pretrained=False,
            num_classes=0,
            img_size=IMG_SIZE,
        )
        bdim = self.backbone.num_features
        for p in self.backbone.parameters():
            p.requires_grad = False

        self.visual_proj = nn.Sequential(
            nn.Linear(bdim, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(512, 256),
        )
        self.color_proj = nn.Sequential(
            nn.Linear(LAB_RAW_DIM, 192),
            nn.LayerNorm(192),
            nn.GELU(),
            nn.Dropout(0.1),
            nn.Linear(192, 102),
        )
        self.classifier = nn.Linear(358, num_classes)

    def forward(self, x, lab_vec=None):
        feat = self.backbone(x)
        vis_emb = F.normalize(self.visual_proj(feat), dim=-1)

        if lab_vec is not None:
            col_emb = F.normalize(self.color_proj(lab_vec), dim=-1)
            fused = F.normalize(torch.cat([vis_emb, col_emb], dim=-1), dim=-1)
        else:
            zeros = torch.zeros(vis_emb.size(0), 102, device=vis_emb.device)
            fused = F.normalize(torch.cat([vis_emb, zeros], dim=-1), dim=-1)

        return self.classifier(fused)


def iter_images(input_dirs):
    for input_dir in input_dirs:
        if not input_dir.exists():
            raise FileNotFoundError(f"Input folder not found: {input_dir}")
        for path in sorted(input_dir.rglob("*")):
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
                yield path


def load_model():
    with SPLITS_PATH.open("rb") as f:
        splits = pickle.load(f)

    family_names = splits["FAMILY_NAMES"]
    model = StoneEmbedder(len(family_names)).to(DEVICE)
    ckpt = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(ckpt["model"])
    model.eval()
    for p in model.parameters():
        p.requires_grad = False
    return model, family_names


def predict_image(model, family_names, image_path):
    img_bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise ValueError(f"Could not read image: {image_path}")

    lab_features = extract_lab_features(img_bgr)
    lab_tensor = torch.from_numpy(lab_features).unsqueeze(0).to(DEVICE)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_tensor = VAL_TF(image=img_rgb)["image"].unsqueeze(0).to(DEVICE)

    with torch.inference_mode():
        logits = model(img_tensor, lab_tensor)
        probs = F.softmax(logits, dim=-1)[0].cpu().numpy()

    top5_indices = np.argsort(probs)[::-1][:5]
    return [family_names[idx] for idx in top5_indices]


def main():
    model, family_names = load_model()
    image_paths = list(iter_images(INPUT_DIRS))

    rows = []
    for index, image_path in enumerate(image_paths, 1):
        top5 = predict_image(model, family_names, image_path)
        rows.append(
            {
                "image name": image_path.name,
                "top 1 prediction": top5[0],
                "prediction 2": top5[1],
                "prediction 3": top5[2],
                "prediction 4": top5[3],
                "prediction 5": top5[4],
            }
        )
        print(f"[{index}/{len(image_paths)}] {image_path.name}: {top5[0]}")

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "image name",
                "top 1 prediction",
                "prediction 2",
                "prediction 3",
                "prediction 4",
                "prediction 5",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
