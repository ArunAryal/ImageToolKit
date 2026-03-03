from PIL import Image
from PIL.ExifTags import TAGS
import io

SENSITIVE_FIELDS={
     "GPSInfo", "Make", "Model", "Software",
    "DateTime", "DateTimeOriginal", "DateTimeDigitized",
    "SerialNumber", "LensSerialNumber", "CameraOwnerName",
    "BodySerialNumber", "MakerNote"
}

# Extract all readable EXIF metadata.Returns empty dict if none found.
def get_metadata(image:Image.Image)-> dict:
    metadata={}
    try:
        exif_data=image._getexif()
        if exif_data:
            for tag_id,value in exif_data.items():
                tag=TAGS.get(tag_id,tag_id)
                if isinstance(value,bytes):
                    try:
                        value=value.decode("utf-8",errors="ignore")
                    except Exception:
                        value="<binary data>"
                metadata[tag]=value
    except Exception:
        pass
    return metadata

#split metadata into sensitive and normal fields
def classify_metadata(metadata:dict)->dict:
    sensitive: dict[str, object] = {}
    normal: dict[str, object] = {}
    for key,value in metadata.items():
        if key in SENSITIVE_FIELDS:
            sensitive[key]=value
        else:
            normal[key]=value
    return {"sensitive":sensitive,"normal":normal}

#Remove all EXIF metadata
def strip_metadata(image:Image.Image)-> io.BytesIO:
    data=image.getdata()
    new=Image.new(image.mode,image.size)
    new.putdata(data)

    fmt=(image.format or "PNG").upper() #fallback if loaded from buffer
    save_fmt="JPEG" if fmt=="JPG" else fmt

    buffer=io.BytesIO()
    new.save(buffer,format=save_fmt)
    buffer.seek(0)
    return buffer