class ListConstant(type):

    def get_list(cls):
        return [v.lower() for k, v in cls.__dict__.items() if k[0].isupper()]

    def get_dict(cls):
        return {k.lower(): v
                for k, v in cls.__dict__.items() if k[0].isupper()}


class TaskStatuses(object, metaclass=ListConstant):
    DownloadPending = "DOWNLOAD_PENDING"
    Processing = "PROCESSING"
    Downloading = "DOWNLOADING"
    Completed = "COMPLETED"
    Error = "ERROR"


class SocketEvents(object, metaclass=ListConstant):
    TaskUpdate = "TASK_UPDATE"


class AllowedFormats(object, metaclass=ListConstant):
    ThreeGP = "3gp"
    AAC = "aac"
    FLV = "flv"
    M4A = "m4a"
    MP3 = "mp3"
    MP4 = "mp4"
    OGG = "ogg"
    WAV = "wav"
    WEBM = "webm"
    MKV = "mkv"


class AudioPP(object, metaclass=ListConstant):
    Best = "best"
    AAC = "aac"
    FLAC = "flac"
    MP3 = "mp3"
    M4A = "m4a"
    OPUS = "opus"
    VORBIS = "vorbis"
    WAV = "wav"


class FormatTypes(object, metaclass=ListConstant):
    Audio = "audio"
    Video = "video"


default_video_format = "mp4"
default_video_height = "720"
default_audio_format = "mp3"
default_audio_bitrate = "256"
video_allowed_height = {"1080": "1080", "720": "720", "480": "480",
                        "360": "360", "240": "240", "144": "144"}
audio_allowed_bitrate = {"320": "320", "256": "256", "192": "192",
                         "160": "160", "128": "128", "96": "96", "32": "32"}
mimetypes = {".mkv": "video/x-matroska", ".webm": "video/webm",
             ".weba": "audio/webm", ".mp4": "video/mp4", ".3gp": "video/3gpp",
             ".aac": "audio/aac", ".flv": "video/x-flv", ".m4a": "audio/m4a",
             ".mp3": "audio/mpeg", ".mp4": "video/mp4", ".oga": "audio/ogg",
             ".wav": "audio/wav", ".flac": "audio/flac", ".opus": "audio/opus",
             ".ogg": "audio/vorbis"}
