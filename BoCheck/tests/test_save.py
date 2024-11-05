import pytest
from BoCheck.save import to_table
from BoCheck.process import process_file
import os

# File path for the test DOCX document
docx_example = "tests/examples/example.docx"

@pytest.fixture
def setup_result():
    """Fixture to process the file and return the result for reuse in tests."""
    result = process_file(docx_example)
    return result

def test_to_table_xlsx(setup_result):
    """Test saving processed data to an XLSX file."""
    result = setup_result
    output_file = 'test_output.xlsx'
    
    # Generate XLSX file and check if it was created successfully
    table_created = to_table(result, output_file)
    assert table_created
    assert os.path.exists(output_file)
    
    # Clean up: Remove the generated XLSX file
    os.remove(output_file)

def test_to_table_csv(setup_result):
    """Test saving processed data to a CSV file."""
    result = setup_result
    output_file = 'test_output.csv'
    
    # Generate CSV file and check if it was created successfully
    table_created = to_table(result, output_file)
    assert table_created
    assert os.path.exists(output_file)
    
    # Clean up: Remove the generated CSV file
    os.remove(output_file)

def test_to_table_errors(setup_result):
    """Test invalid inputs for the to_table function."""
    result = setup_result
    
    # Attempting to save to an unsupported or invalid file format
    with pytest.raises(ValueError):
        to_table(result, 'test_output.pdf')
        to_table(result, 'test_output.img')
    
    # Invalid data types as input
    with pytest.raises(ValueError):
        to_table(123, 'test_output.xlsx')
        to_table('invalid_data', 'test_output.csv')

    # Invalid output file extensions
    with pytest.raises(ValueError):
        to_table(result, 'test_output.unknown')

def test_process_file_errors():
    """Test process_file with invalid inputs."""
    
    # Attempting to process a non-existent or invalid file
    with pytest.raises(ValueError):
        process_file('invalid_path.docx')

    # Passing an invalid file type
    with pytest.raises(ValueError):
        process_file(123)
        process_file('invalid_text')

def test_invalid_paths_for_to_table(setup_result):
    """Test handling of invalid file paths for to_table function."""
    result = setup_result
    
    # Non-writable or non-existent directory
    with pytest.raises(OSError):
        to_table(result, '/non_existent_dir/test_output.xlsx')

def test_empty_result_to_table():
    """Test handling of empty results in to_table function."""
    empty_result = []
    
    # Attempting to save an empty result to XLSX or CSV should raise an error
    with pytest.raises(ValueError):
        to_table(empty_result, 'test_output.xlsx')
        to_table(empty_result, 'test_output.csv')

        
if __name__ == "__main__":
    pytest.main()
