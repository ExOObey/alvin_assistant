from setuptools import setup, find_packages

setup(
    name='alvin-assistant',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ollama', 'asyncio', 'websockets', 'pyaudio', 'torch', 'Flask',
        'porcupine', 'sounddevice', 'huggingface_hub', 'transformers',
        'pytesseract', 'pyautogui', 'Pillow', 'psutil', 'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'alvin=main:main',
        ],
    },
    author='Your Name',
    description='Alvin AI Assistant',
    license='MIT',
)
