import streamlit as st
import qrcode
import io

def main():
    st.title("UR-Code: QR Code Generator")
    with st.form("QR Codes Form"):
        data = st.text_input("Enter the data for the QR code")
        qr_color = st.color_picker("Select QR Code Color", "#000000")
        bg_color = st.color_picker("Select Background Color", "#FFFFFF")
        submit_button = st.form_submit_button("Generate QR Code")

    if submit_button:
        if data:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color=qr_color, back_color=bg_color)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            st.image(buffer.getvalue(), caption="Generated QR Code", use_container_width=True)
        else:
            st.error("Please enter some data to generate a QR code.")

if __name__ == "__main__":
    main()