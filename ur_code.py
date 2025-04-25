import streamlit as st
import qrcode
import io
from PIL import Image

def recolor_icon(icon_path, hex_color):
    icon = Image.open(icon_path).convert("RGBA")
    rgb_color = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    r, g, b, alpha = icon.split()
    solid_color = Image.new("RGBA", icon.size, rgb_color + (0,))
    colored_icon = Image.composite(solid_color, icon, alpha)
    colored_icon.putalpha(alpha)

    return colored_icon

def generate_qr_with_icon(data, qr_color, bg_color, icon_img):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H, 
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')

    # Resize icon
    icon_size = int(img.size[0] * 0.2)
    icon_img = icon_img.resize((icon_size, icon_size), Image.LANCZOS)

    pos = ((img.size[0] - icon_size) // 2, (img.size[1] - icon_size) // 2)
    img.paste(icon_img, pos, mask=icon_img)

    return img

def main():
    st.title("UR-Code: QR Code Generator")

    with st.form("QR Codes Form"):
        data = st.text_input("Enter the link to be QR-ified!")
        qr_color = st.color_picker("Select QR Code Color", "#000000")
        bg_color = st.color_picker("Select Background Color", "#FFFFFF")
        icon__select = st.selectbox("Select Icon", ["Medicine Logo", "Yellow Jacket"])
        icon_color = st.color_picker("Select Icon Color", "#FFD700") 
        submit_button = st.form_submit_button("Generate QR Code")

    if submit_button:
        if data:
            if icon__select == "Medicine Logo":
                icon_path = "ur_crest.png" 
            elif icon__select == "Yellow Jacket":
                icon_path = "yellow_jacket_icon.png" 
            colored_icon = recolor_icon(icon_path, icon_color)
            final_img = generate_qr_with_icon(data, qr_color, bg_color, colored_icon)

            buffer = io.BytesIO()
            final_img.save(buffer, format="PNG")
            st.image(buffer.getvalue(), caption="Generated QR Code", use_container_width=True)
        else:
            st.error("Please enter some data to generate a QR code.")

if __name__ == "__main__":
    main()