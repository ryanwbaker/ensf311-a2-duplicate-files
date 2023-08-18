import duplicates_cli as dc
import pytest

def test_get_hash_md5():
    import hash_functions
    filename = 'files/test.txt'
    with open(filename, 'rb') as fin:
        message = fin.read()

    assert dc.get_hash(filename) == hash_functions.hashmd5(message)

def test_no_args_passed(capsys):
    expected_out_parts = ["[-h] [-e EXTENSION]", "dirname",
                    "error: the following arguments are required: dirname"]
    
    with pytest.raises(SystemExit):
        dc.cli([])

    captured = capsys.readouterr()
    result = captured.err
    result = result.splitlines()
    result = [line.strip() for line in result]
    assert expected_out_parts[0] in result[0] 
    assert expected_out_parts[1] in result[1] 

def test_extension_pdf_output(capsys):
    expected_out = ["These files have the same hash:",
                    "files/archive/sines_archive.pdf",
                    "files/fig/sines.pdf",
                    "files/sines.pdf"]
    
    dc.cli(['-e', '.pdf', 'files'])

    captured = capsys.readouterr()
    result = captured.out
    result = result.splitlines()
    result = [line.strip() for line in result]
    result = [line.replace('\\', '/') for line in result]
    assert result == expected_out

def test_full_output(capsys):
    
    expected_out = ["These files have the same hash:",
                    "files/archive/sines_archive.pdf",
                    "files/fig/sines.pdf",
                    "files/sines.pdf",
                    "These files have the same hash:",
                    "files/archive/test_archive.txt",
                    "files/test.txt",
                    "files/test_copy.txt",
                    "files/txt/test.txt",
                    "files/txt/test_copy.txt",
                    "These files have the same hash:",
                    "files/test2.txt", 
                    "files/txt/test2.txt"]

    dc.cli(['files'])

    captured = capsys.readouterr()
    result = captured.out
    result = result.splitlines()
    result = [line.strip() for line in result]
    result = [line.replace('\\', '/') for line in result]
    assert result == expected_out