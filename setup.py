from setuptools import setup, find_packages


setup(
    name='jotason',
    version='1.0',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        # System dependencies
        # Ubuntu:
        #     sox libsox-fmt-mp3 python3-dev libasound2-dev portaudio19-dev
        #     libportaudio2 libportaudiocpp0
        # Arch Linux:
        #    sox twolame portaudio
        'google_speech',
        'SpeechRecognition',
        'pyaudio'
    ],
    entry_points={
        'console_scripts': ['jotason = jotason.__main__:main']
    }
)
