import qrcode
import io
from fastapi.responses import StreamingResponse

def generate_qr_png(url: str) -> StreamingResponse:
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
