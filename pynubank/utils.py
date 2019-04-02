from qrcode import QRCode


def print_qr_code(uuid: str):
    qr = QRCode()
    qr.add_data(uuid)
    try:
        get_ipython
        from IPython.display import display
        display(qr.make_image(fill_color="#111", back_color="#ccc"))
    except NameError:
        qr.print_ascii(invert=True)