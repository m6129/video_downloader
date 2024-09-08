import streamlit as st

from pathlib import Path

from src.helpers import download_rt_video, download_yt_video, SAMPLE_URL, RUTUBE_KEY, VK_KEY

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'src/styles/.css'

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = 'Video Downloader'
PAGE_ICON: str = ':tv:'


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


def download_video(url: str):
    if url:
        if RUTUBE_KEY in url:
            download_rt_video(url)
        elif VK_KEY in url:
            st.warning('VK Video Downloading is not supported yet.')
            # download_vk_video(url)
        else:
            download_yt_video(url)


def main() -> None:
    video_url: str = st.text_input(label='Input Video URL:', value=SAMPLE_URL)
    download_video(url=video_url)
    line()


if __name__ == '__main__':
    main()
