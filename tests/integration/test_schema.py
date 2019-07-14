"""
Validate the output XML file against the schema
"""
import os
import xmlschema
from xml.etree import ElementTree


def test_sample_file_against_reference_schema(testdir, tmpdir):
    """
    Test the example.xml file against the schema in the Nunit3 source
    """
    my_path = os.path.abspath(os.path.dirname(__file__))
    xs = xmlschema.XMLSchema(os.path.join(my_path, '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    xt = ElementTree.parse(os.path.join(my_path, '../../example.xml'))
    assert xs.is_valid(xt), xs.validate(xt)


def test_basic_against_reference_schema(testdir, tmpdir):
    """
    Test a basic output against the schema in the Nunit3 source
    """
    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_basic():
            assert 1 == 1
    """)
    outfile=os.path.join(tmpdir, 'out.xml')

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_basic PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

    # ensure the output file exists
    os.path.exists(outfile)

    my_path = os.path.abspath(os.path.dirname(__file__))
    xs = xmlschema.XMLSchema(os.path.join(my_path, '../../ext/nunit-src/TestResult.xsd'), validation='lax')
    xt = ElementTree.parse(outfile)
    assert xs.is_valid(xt), xs.validate(xt)

def test_model_schema(testdir, tmpdir):
    """
    Test a basic output against the schema created for parsing models
    """
    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_basic():
            assert 1 == 1
    """)
    outfile=os.path.join(tmpdir, 'out.xml')

    # run pytest with the following cmd args
    result = testdir.runpytest(
        '-v', '--nunit-xml='+outfile
    )

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*test_basic PASSED*',
    ])

    # make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0

    # ensure the output file exists
    os.path.exists(outfile)

    my_path = os.path.abspath(os.path.dirname(__file__))
    xs = xmlschema.XMLSchema(os.path.join(my_path, '../../ext/nunit-model/TestResult.xsd'), validation='lax')
    xt = ElementTree.parse(outfile)
    assert xs.is_valid(xt), [error for error in xs.iter_errors(xt)]

