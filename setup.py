from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst')
    )


install_requires = [
    'grok',
    'setuptools',
    'zope.component',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.schema',
    ]


tests_require = [
    ]


setup(
    name='megrok.paypal',
    version='0.1.dev0',
    author='Uli Fouquet',
    author_email='uli@gnufix.de',
    url='http://github.com/ulif/megrok.paypal',
    download_url='http://pypi.python.org/pypi/megrok.paypal',
    description='PayPal support for Grok/Zope.',
    long_description=long_description,
    license='GPL 3.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        (
            'License :: OSI Approved :: '
            'GNU General Public License v3 or later (GPLv3+)'),
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
    ],

    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['megrok'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='megrok.paypal.tests.test_megrok_paypal.test_suite',
    tests_require=tests_require,
    extras_require={'test': tests_require},
)
