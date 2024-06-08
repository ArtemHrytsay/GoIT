import hashlib
import cloudinary
import cloudinary.uploader

from src.conf.config import settings as s


class CloudImage:
    cloudinary.config(
        cloud_name = s.cloudinary_name,
        api_key    = s.cloudinary_api_key,
        api_secret = s.cloudinary_api_secret,
        secure=True
    )

    @staticmethod
    def generate_name_avatar(email: str):
        name = hashlib.sha256(email.encode('utf-8')).hexdigest()[:12]
        return name

    @staticmethod
    def upload(file, public_id: str):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_url_for_avatar(public_id, r):
        src_url = cloudinary.CloudinaryImage(public_id) \
            .build_url(width=250, height=250, crop='fill', version=r.get('version'))
        return src_url
