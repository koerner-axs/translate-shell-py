import subprocess


def init_audio_player():
    """Initialize audio player by checking availability of various players."""
    try:
        # Check for mpv
        if subprocess.call(['mpv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            return 'mpv --no-config'
        # Check for mplayer
        elif subprocess.call(['mplayer'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            return 'mplayer'
        # Check for mpg123
        elif subprocess.call(['mpg123', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
            return 'mpg123'
        else:
            return ''
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ''


def play_remote_audio(player: str, url: str):
    # TODO: support backup local speech synthesizer
    if code := subprocess.call([*player.split(), url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        print(f'Playing audio failed with return code: {code}')
