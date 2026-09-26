"""
hand.py
Modul untuk deteksi tangan & pengenalan gestur menggunakan MediaPipe.
"""

import math
import mediapipe as mp


class HandTracker:
    def __init__(self, max_hands=1, detection_conf=0.6, tracking_conf=0.6):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf,
        )

    def process(self, frame_rgb):
        """Jalankan deteksi tangan pada satu frame (format RGB)."""
        return self.hands.process(frame_rgb)

    def draw_landmarks(self, frame_bgr, hand_landmarks):
        """Gambar titik & garis skeleton tangan di atas frame."""
        self.mp_draw.draw_landmarks(
            frame_bgr,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_draw.DrawingSpec(color=(138, 255, 57), thickness=2, circle_radius=3),
            self.mp_draw.DrawingSpec(color=(214, 47, 255), thickness=2),
        )

    @staticmethod
    def _distance(a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

    def count_fingers(self, landmarks):
        """Hitung jumlah jari yang terbuka (0-5) dari 21 titik landmark."""
        lm = landmarks.landmark
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        count = 0
        for tip, pip in zip(tips, pips):
            if lm[tip].y < lm[pip].y:
                count += 1

        # Ibu jari: bandingkan jarak ujung vs sendi terhadap pergelangan tangan
        wrist = lm[0]
        if self._distance(lm[4], wrist) > self._distance(lm[3], wrist) * 1.05:
            count += 1

        return count

    def is_pinching(self, landmarks, threshold=0.35):
        """Deteksi gestur pinch (jempol & telunjuk berdekatan)."""
        lm = landmarks.landmark
        hand_size = self._distance(lm[0], lm[9])
        if hand_size == 0:
            return False
        pinch_dist = self._distance(lm[4], lm[8]) / hand_size
        return pinch_dist < threshold

    def close(self):
        self.hands.close()
