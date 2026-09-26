"""
main.py
Program utama: hand tracking dengan filter visual berbasis gestur,
mirip demo di video (mode selfie + filter berubah sesuai gestur tangan).
"""

import cv2
from hand import HandTracker
from selfie import mirror, get_filter_for_gesture, draw_hud


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Tidak bisa membuka webcam. Pastikan kamera tersedia & tidak dipakai app lain.")
        return

    tracker = HandTracker(max_hands=1)

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = mirror(frame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = tracker.process(frame_rgb)

        mode_label = "NO HAND"
        filter_name = "NORMAL"
        output = frame

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            fingers = tracker.count_fingers(hand_landmarks)
            pinching = tracker.is_pinching(hand_landmarks)

            filter_name, filter_fn = get_filter_for_gesture(fingers, pinching)
            output = filter_fn(frame)

            tracker.draw_landmarks(output, hand_landmarks)
            mode_label = "PINCH" if pinching else f"{fingers} JARI TERBUKA"
        else:
            _, filter_fn = get_filter_for_gesture(5, False)
            output = filter_fn(frame)

        draw_hud(output, mode_label, filter_name)
        cv2.imshow("Hand Tracking Filter", output)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tracker.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
