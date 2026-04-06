"""
webcam_capture.py  —  Script auxiliar para captura aislada de webcam.
Se ejecuta como subprocess SEPARADO del kernel de Jupyter para que
cualquier crash de driver no mate el kernel principal.

Uso:
    python webcam_capture.py <output_path.png> [camera_index]

Retorna:
    exit code 0  → imagen guardada correctamente en output_path
    exit code 1  → error (imprime mensaje en stderr)
"""
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Uso: python webcam_capture.py <output.png> [cam_index]", file=sys.stderr)
        sys.exit(1)

    output_path = sys.argv[1]
    cam_index   = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    # Importar cv2 aqui — si da segfault, solo muere este proceso
    try:
        import cv2
    except ImportError as e:
        print(f"cv2 no disponible: {e}", file=sys.stderr)
        sys.exit(1)

    # Intentar primero con CAP_DSHOW (Windows DirectShow), luego backend generico
    backends = [cv2.CAP_DSHOW, cv2.CAP_ANY]
    for backend in backends:
        cap = None
        try:
            cap = cv2.VideoCapture(cam_index, backend)
            if not cap.isOpened():
                if cap: cap.release()
                continue
            # Leer varios frames para que la camara se "caliente"
            for _ in range(3):
                cap.read()
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                cv2.imwrite(output_path, frame)
                print(f"OK:{output_path}")
                sys.exit(0)
        except Exception as e:
            if cap:
                try: cap.release()
                except: pass
            print(f"Backend {backend} fallo: {e}", file=sys.stderr)
            continue

    print("No se pudo capturar imagen con ningun backend", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
