import streamlit as st
from pathlib import Path
from yt_dlp import YoutubeDL

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
css_file = current_dir / 'src/styles/.css'

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = 'Video Downloader'
PAGE_ICON: str = ':tv:'
SAMPLE_URL: str = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
RUTUBE_KEY: str = 'rutube'
VK_KEY: str = 'vk.com'

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

def download_yt_video(url: str):
    try:
        with st.spinner('Загрузка видео...'):
            ydl_opts = {
                'format': 'best',  # Лучшее качество
                'outtmpl': '%(title)s.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            # Получаем информацию о видео
            with YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)
                title = video_info.get('title', 'video')
                formats = video_info.get('formats', [])
                
                # Создаем список доступных разрешений
                resolutions = list(set([f.get('height', 0) for f in formats if f.get('height')]))
                resolutions.sort(reverse=True)
                
                # Выбор разрешения
                selected_resolution = st.selectbox(
                    'Выберите разрешение:',
                    resolutions,
                    format_func=lambda x: f'{x}p'
                )
                
                if st.button('Скачать'):
                    # Обновляем настройки для выбранного разрешения
                    ydl_opts.update({
                        'format': f'bestvideo[height<={selected_resolution}]+bestaudio/best[height<={selected_resolution}]'
                    })
                    
                    # Скачиваем видео
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    st.success(f'Видео "{title}" успешно скачано!')
                    
    except Exception as e:
        st.error(f'Ошибка при скачивании: {str(e)}')

def download_rt_video(url: str):
    st.warning('Скачивание видео с Rutube пока не поддерживается')

def download_video(url: str):
    if url:
        if RUTUBE_KEY in url:
            download_rt_video(url)
        elif VK_KEY in url:
            st.warning('Скачивание видео с VK пока не поддерживается')
        else:
            download_yt_video(url)

def main() -> None:
    video_url: str = st.text_input(label='Введите URL видео:', value=SAMPLE_URL)
    download_video(url=video_url)
    line()

if __name__ == '__main__':
    main()
