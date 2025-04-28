import threading
import time
import cv2
from mjpeg_streamer import MjpegServer, Stream
from nicegui import ui

def run_camera():
    cap = cv2.VideoCapture(0)
    stream = Stream(
        name="my_camera",
        size=(640, 480),
        quality=50,
        fps=30
    )
    server = MjpegServer("0.0.0.0", 8080)
    server.add_stream(stream)
    server.start()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        stream.set_frame(frame)
        time.sleep(0.01)

    server.stop()
    cap.release()

@ui.page('/')
def index_page():
    ui.add_head_html("""
    <link
      href="https://cdn.jsdelivr.net/npm/tailwindcss@3.3.2/dist/tailwind.min.css"
      rel="stylesheet"
    />
    <style>
      /* NiceGUI varsayılan arkaplanını koyu yapalım */
      html, body, .q-page {
          margin: 0;
          padding: 0;
          background-color: #121212 !important; /* Koyu arka plan */
          color: #FFFFFF !important;           /* Beyaz metin */
      }
    </style>
    """)

    with ui.column().classes('w-full max-w-4xl mx-auto mt-10 space-y-4'):
        ui.label('Kamera ve Sensör Verileri').classes(
            'text-3xl font-bold'
        )

        # Sensör bilgilerinin yatayda sıralanması
        with ui.row().classes('justify-center space-x-8'):
            ui.label('Temperature: 25°C').classes('text-lg')
            ui.label('pH: 7.2').classes('text-lg')
            ui.label('Humidity: 55%').classes('text-lg')

        # Kamera akışını iframe ile ekle
        ui.html('''
            <iframe
                src="http://127.0.0.1:8080/my_camera"
                width="480"
                height="360"
                class="rounded shadow-lg border-2 border-gray-600"
            ></iframe>
        ''')


camera_thread = threading.Thread(target=run_camera, daemon=True)
camera_thread.start()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host="0.0.0.0", port=5000)
