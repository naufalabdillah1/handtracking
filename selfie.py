"""
selfie.py
Modul untuk efek filter visual pada frame webcam (mode selfie/mirror)
dan overlay teks HUD (mode & filter aktif), meniru tampilan di video.
"""

import time
import cv2
import numpy as np


def mirror(frame):
    """Balik frame secara horizontal agar terasa seperti cermin (selfie)."""
    return cv2.flip(frame, 1)


def apply_invert(frame):
    return cv2.bitwise_not(frame)


def apply_sepia(frame):
    kernel = np.array([[0.272, 0.534, 0.131],
                        [0.349, 0.686, 0.168],
                        [0.393, 0.769, 0.189]])
    sepia = cv2.transform(frame, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)


def apply_grayscale(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_blur(frame):
    return cv2.GaussianBlur(frame, (25, 25), 0)


def apply_rainbow(frame):
    """Filter warna berputar (hue shift) seperti efek 'rainbow wave'."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int16)
    shift = int((time.time() * 60) % 180)
    hsv[:, :, 0] = (hsv[:, :, 0] + shift) % 180
    hsv = hsv.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


FILTERS = {
    0: ("INVERT", apply_invert),
    1: ("SEPIA", apply_sepia),
    2: ("GRAYSCALE", apply_grayscale),
    3: ("BLUR", apply_blur),
    5: ("NORMAL", lambda f: f),
}


def get_filter_for_gesture(fingers, pinching):
    """Pilih filter berdasarkan jumlah jari terbuka / gestur pinch."""
    if pinching:
        return "RAINBOW WAVE", apply_rainbow
    return FILTERS.get(fingers, ("NORMAL", lambda f: f))


def draw_hud(frame, mode_label, filter_name):
    """Gambar teks 'MODE:' dan 'FILTER:' di pojok kiri atas, gaya HUD."""
    cv2.putText(frame, f"MODE: {mode_label}", (14, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (47, 255, 247), 2, cv2.LINE_AA)
    cv2.putText(frame, f"FILTER: {filter_name}", (14, 54),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (214, 47, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "q = keluar", (14, frame.shape[0] - 14),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1, cv2.LINE_AA)
