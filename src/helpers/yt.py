import streamlit as st

from urllib.error import URLError

from pytube import YouTube
from pendulum import Duration
from pytube.exceptions import RegexMatchError, VideoUnavailable

from src.helpers.const import MIME, SAVE_PATH, DEFAULT_NAME
from src.helpers.utils import show_video, download_video_locally


@st.cache_data
def search_yt_resolution(video_url: str, progressive: bool) -> list[str]:
    try:
        video = YouTube(video_url)
        resolutions = [i.resolution for i in video.streams.filter(mime_type=MIME, progressive=progressive)]
        return sorted(set(resolutions), reverse=True)
    except (URLError, RegexMatchError, VideoUnavailable) as err:
        st.error(err)


def prepare_yt_video(video_url: str, resolution: str, progressive: bool) -> str | None:
    with st.form('prepare_yt_video'):
        if st.form_submit_button('Prepare Video'):
            with st.spinner('Preparing Video ...'):
                try:
                    video = YouTube(url=video_url)
                    if video:
                        title = video.title
                        st.write(f'Title: `{title}`')
                        st.write(f'Publish Date: `{video.publish_date}`')
                        st.write(f'Duration: `{Duration(seconds=video.length)}`')
                        st.write(f'Views: `{video.views}`')
                        video.streams.filter(
                            res=resolution,
                            progressive=progressive,
                        ).first().download(
                            output_path=SAVE_PATH,
                            filename=DEFAULT_NAME,
                        )
                        st.success('Video Prepared Successfully.')
                        return title
                except URLError as err:
                    st.error(err)


def download_yt_video(url: str):
    show_video(data=url)
    with st.spinner('Update Resolutions List ...'):
        c1, c2, _ = st.columns(3)
        progressive_res = c1.checkbox(label='Use Progressive Resolutions', value=True)
        resolutions = search_yt_resolution(video_url=url, progressive=progressive_res)
        resolution = c2.selectbox(label='Select Video Resolution:', options=resolutions or [])

    title = prepare_yt_video(video_url=url, resolution=resolution, progressive=progressive_res)
    download_video_locally(title=title)
