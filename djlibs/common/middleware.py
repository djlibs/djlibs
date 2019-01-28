"""
Estonian ID-card authentication middleware for Django,
but this should be pretty easily modifiable for any application
To use install cryptography.io:
    apt-get install -y python python-pip python-dev \
        python-cffi build-essential libffi-dev libssl-dev
    pip install cryptography
For nginx use following to pass the certificate with CGI headers
  uwsgi_param SSL_CLIENT_CERT $ssl_client_raw_cert;
"""

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import ExtensionOID, NameOID
from cryptography.x509.general_name import RFC822Name
from django.contrib.auth.models import User

class CertificateAuthMiddleware(object):
    def process_request(self, req):
        if req.user.is_authenticated(): # Rely on cookies!
            return
        crt = x509.load_pem_x509_certificate(   
            req.META.get("SSL_CLIENT_CERT"),
            backend=default_backend())
        for name in crt.subject:
            if name.oid == NameOID.GIVEN_NAME:
                gn = name.value
            elif name.oid == NameOID.SURNAME:
                sn = name.value
            elif name.oid == NameOID.SERIAL_NUMBER:
                serial = name.value
        try:
            req.user = User.objects.get(username=serial)
        except User.DoesNotExist:
            for extension in crt.extensions:
                if extension.oid == ExtensionOID.SUBJECT_ALTERNATIVE_NAME:
                    for name in extension.value:
                        if isinstance(name, RFC822Name):
                            email = name.value
            req.user = User.objects.create(
                email = email,
                first_name = gn,
                last_name = sn,
                username = serial)