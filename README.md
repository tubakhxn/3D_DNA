# dna_visualizer_air_gestures

Real-time, gesture-controlled 3D DNA visualizer using your webcam.

Created and developed by @tubakhxn.

---

## Quickstart — fork, install, run

1. Fork this repository on GitHub and clone it locally:

   ```powershell
   git clone https://github.com/<your-username>/dna_visualizer_air_gestures.git
   cd dna_visualizer_air_gestures
   ```

2. Create and activate a Python virtual environment (Windows PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Run the app (webcam required for live gestures; keyboard fallbacks included):

   ```powershell
   python main.py
   ```

Controls:
- Press `W` to toggle the external webcam preview window (useful to see yourself while gesturing).
- Press `D` to toggle debug overlays.
- Keyboard fallbacks are available if no webcam is present (see on-screen instructions).

---

## Gestures (short list)
- two_finger_rotate — rotate/twist the DNA (fallback: `R`/`T`)
- pinch_zoom — pinch to zoom (fallback: `Z`/`X`)
- two_hand_stretch — uncoil/coil (fallback: `U`/`J`)
- finger_point — inspect/select (fallback: `P`)
- clap — replication trigger (fallback: `SPACE`)

See `core/gesture_engine.py` for full gesture heuristics and `ui/overlay.py` for on-screen controls.

---

## License

This project is released under the MIT License. See the `LICENSE` file on GitHub for full text.

If you publish a fork or derivative, please keep the original credit: Created and developed by @tubakhxn.


