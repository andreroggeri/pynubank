import builtins

import pytest
from qrcode import QRCode

from pynubank import utils


@pytest.mark.skip(reason="no way of currently testing this")
def test_print_qr_code_on_jupyter_prints_image(monkeypatch):
    def fake_print(x):
        raise Exception('Should not call print')

    def fake_ipython():
        pass

    try:
        builtins.get_ipython = fake_ipython

        monkeypatch.setattr('builtins.print', fake_print)
        utils.print_qr_code('some-uuid-1234')
    finally:
        del (builtins.get_ipython)


def test_print_qr_code_on_terminal_prints_ascii():
    def fake_make_image(self, image_factory=None, **kwargs):
        raise Exception('Should not call make_image')

    QRCode.make_image = fake_make_image
    utils.print_qr_code('some-uuid-1234')
