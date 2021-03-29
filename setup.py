from setuptools import setup

with open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='liasis',
    version='0.1dev0',
    url='https://github.com/Saegl/liasis',
    author='Saegl',
    author_email='saegl@protonmail.com',
    packages=['liasis'],
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    long_description=readme,
    python_requires='>=3.6',
    install_requires=[
        'attrs==17.4.0',
        'click==6.7',
        'colorama==0.3.9',
        'lark-parser==0.5.5',
        'prompt-toolkit==2.0.4',
        'Pygments==2.7.4',
        'six==1.11.0',
        'wcwidth==0.1.7',
    ],
    entry_points={
        'console_scripts': [
            'liasis = liasis.app:main'
        ]
    }
)
