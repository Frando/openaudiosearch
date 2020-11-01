from pydantic import BaseModel
from typing import Any, List
from enum import Enum


class Engine(str, Enum):
    vosk = "vosk"
    pytorch = "pytorch"
    foo = 'foo'


class DownloadArgs(BaseModel):
    media_url: str


class DownloadOpts(BaseModel):
    refresh = False


class DownloadResult(BaseModel):
    source_url: str
    file_path: str


class PrepareOpts(BaseModel):
    samplerate = 16000


class AsrArgs(BaseModel):
    file_path: str


class AsrOpts(BaseModel):
    engine: Engine
    language: str = 'de'


class AsrResult(BaseModel):
    text: str
    parts: List[Any]


class NlpOpts(BaseModel):
    pipeline: str = 'ner,pos,lemma,missed'


class NlpResult(BaseModel):
    result: dict


class TranscribeArgs(BaseModel):
    media_url: str


class TranscribeOpts(PrepareOpts, AsrOpts, NlpOpts):
    pass


    # this is used by the CLI
TASKS = {
    'transcribe': (TranscribeArgs, TranscribeOpts),
    'download': (DownloadArgs, DownloadOpts),
}
