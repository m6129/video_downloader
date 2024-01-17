from urllib.error import URLError

import streamlit as st

from pathlib import Path
from pytube import YouTube
from pendulum import Duration
from pytube.exceptions import RegexMatchError
from streamlit.runtime.media_file_storage import MediaFileStorageError

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'src/styles/.css'

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = 'YouTube Downloader'
PAGE_ICON: str = ':tv:'
SAMPLE_URL: str = 'https://www.youtube.com/watch?v=8HZ4DnVfWYQ'
MIME: str = 'video/mp4'
DEFAULT_EXT: str = 'mp4'
DEFAULT_NAME: str = f'video.{DEFAULT_EXT}'
SAVE_PATH: str = '.'

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


def write_md(body: str) -> None:
    st.markdown(body=body, unsafe_allow_html=True)


def line() -> None:
    st.markdown('---')


# --- LOAD CSS ---
with open(css_file) as f:
    write_md('<style>{}</style>'.format(f.read()))

write_md(f'''<h1 style='text-align: center;'>{PAGE_TITLE}</h1>''')
line()


@st.cache_data
def search_resolution(video_url: str, progressive: bool) -> list[str]:
    try:
        video = YouTube(video_url)
        resolutions = [i.resolution for i in video.streams.filter(mime_type=MIME, progressive=progressive)]
        return sorted(set(resolutions), reverse=True)
    except (URLError, RegexMatchError) as err:
        st.error(err)


def prepare_video(video_url: str, resolution: str, progressive: bool) -> str | None:
    with st.form('prepare_video'):
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


def main() -> None:
    video_url: str = st.text_input(label='Input Video URL:', value=SAMPLE_URL)
    if video_url:
        try:
            st.video(video_url)
        except MediaFileStorageError as err:
            st.error(err)
        with st.spinner('Update Resolutions List ...'):
            c1, c2, _ = st.columns(3)
            progressive_res = c1.checkbox(label='Use Progressive Resolutions', value=True)
            resolutions = search_resolution(video_url=video_url, progressive=progressive_res)
            resolution = c2.selectbox(label='Select Video Resolution:', options=resolutions or [])

        title = prepare_video(video_url=video_url, resolution=resolution, progressive=progressive_res)
        if title:
            with open(DEFAULT_NAME, 'rb') as file:
                if st.download_button('Download', data=file, file_name=f'{title}.{DEFAULT_EXT}', mime=MIME):
                    with st.spinner('Downloading Video ...'):
                        st.success('Video Downloaded Successfully.')
    line()


if __name__ == '__main__':
    main()
