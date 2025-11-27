import cv2
import os

def test_camera(index=0, out='webcam_test.jpg'):
    cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f'ERROR: Could not open camera index {index}')
        return 2
    ret, frame = cap.read()
    if not ret:
        print('ERROR: Failed to read frame from camera')
        cap.release()
        return 3
    # Save frame
    cv2.imwrite(out, frame)
    h, w = frame.shape[:2]
    print(f'SUCCESS: Captured frame {w}x{h} to "{out}"')
    cap.release()
    return 0

if __name__ == '__main__':
    import sys
    idx = 0
    if len(sys.argv) > 1:
        try:
            idx = int(sys.argv[1])
        except Exception:
            idx = 0
    exit_code = test_camera(idx)
    sys.exit(exit_code)
