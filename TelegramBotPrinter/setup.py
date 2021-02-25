from setuptools import setup

setup(
    name='TelegramBorPrinter',
    version='0.1dev',
    packages=['telegram_bot_printer', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    scripts=['bin/run_bot_telegram'],
    include_package_data=True,
    package_data={'': ['config/config.toml', 'config/log_config.yaml']},
    install_requires=[
        'toml',
        'pyyaml',
        'python-telegram-bot',
    ]
)
