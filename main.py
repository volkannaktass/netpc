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
      /* NiceGUI varsayılan arkaplanını geçersiz kılmak için */
      html, body, .q-page {
          margin: 0;
          padding: 0;
          background-color: #121212 !important; /* Tam koyu renk */
          color: #FFFFFF !important;            /* Yazı rengi */
      }
    </style>
    """)

    with ui.column().classes('items-center justify-center min-h-screen'):
        ui.label('Kamera ve Sensör Verileri').classes(
            'text-3xl font-bold mb-4 text-gray-50'
        )

        with ui.row().classes('justify-around w-full max-w-xl mb-4'):
            ui.label('Temperature: 25°C').classes('text-xl text-gray-50')
            ui.label('pH: 7.2').classes('text-xl text-gray-50')
            ui.label('Humidity: 55%').classes('text-xl text-gray-50')

        ui.html('''
            <iframe 
                src="http://127.0.0.1:8080/my_camera" 
                width="640" 
                height="480"
                class="rounded shadow-lg border-2 border-gray-500">
            </iframe>
        ''')

camera_thread = threading.Thread(target=run_camera, daemon=True)
camera_thread.start()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(host="0.0.0.0", port=5000)
