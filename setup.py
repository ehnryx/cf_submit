from setuptools.command.install import install
from setuptools import setup, dist


def pre_install():
    import os
    os.system('pip install -r cf_submit/requirements.txt')


def post_install():
    import os
    print("Copying cf_ckecher to /usr/bin")
    os.system('cp cf_submit/cf_checker /usr/bin')
    print("Copying auto_complete_cf to /etc/bash_completion.d")
    os.system('cp cf_submit/auto_complete_cf /etc/bash_completion.d')
    os.system('source /etc/bash_completion.d/auto_complete_cf')


class CustomInstallCommand(install):
    def run(self):
        pre_install()
        install.run(self)
        post_install()


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cf_submit",
    version="1.0.2",
    scripts=['cf'],
    author="Nasreddine Bac Ali",
    author_email="nasreddine.bacali95@gmail.com",
    description="Submit Codeforces codes via terminal and other coll stuff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bacali95/cf_submit",
    packages=['cf_submit'],
    package_data={
        'cf_submit': [
            'cf_checker',
            'auto_complete_cf',
            'hack_prob.sh'
        ]
    },
    install_requires=[
        'lxml',
        'robobrowser',
        'prettytable',
        'javalang'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], cmdclass={
        'install': CustomInstallCommand
    }
)
