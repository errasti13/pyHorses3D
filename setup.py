from setuptools import setup, find_packages

setup(
    name='pyHorses3D',
    version='0.2.0',
    description='Python interface for the Horses3D CFD solver',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jon Errasti',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/pyHorses3D',
    packages=find_packages(),
    install_requires=[
        'matplotlib>=3.7.0',
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'setuptools>=65.0.0'
    ],
    entry_points={
        'console_scripts': [
            'pyhorses3d=pyHorses3D.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)
