import numpy as np
import pytest
from BoCheck.memristor.memristor import memristor


@pytest.fixture
def memristor_instance():
    """
    Create an instance of the memristor class to use in tests.
    """
    return memristor()

def test_dx(memristor_instance):
    """
    Test the dx function for expected changes based on input voltage.
    """
    v_pos = 0.6  # positive voltage, should increase state
    v_neg = -0.6  # negative voltage, should decrease state
    zero = 0  # zero voltage, should have no effect
    
    assert memristor_instance.dx(v_pos) > 0
    assert memristor_instance.dx(v_neg) < 0
    assert memristor_instance.dx(zero) == 0

def test_R(memristor_instance):
    """
    Test the R function to ensure it calculates resistance based on state.
    """
    memristor_instance.x = 1  # fully on (Ron)
    assert memristor_instance.R() == memristor_instance.Ron
    
    memristor_instance.x = 0  # fully off (Roff)
    assert memristor_instance.R() == memristor_instance.Roff

def test_update_x(memristor_instance):
    """
    Test the update_x function to ensure the state updates correctly
    and adheres to the limits set by x_on and x_off.
    """
    # Case 1: Positive update
    memristor_instance.x = 1
    dt = 0.01
    dx = 0.5
    updated_x = memristor_instance.update_x(dt, dx)
    expected_x = min(memristor_instance.x_on, 1 + dt * dx)
    assert updated_x == expected_x

    # Case 2: Negative update
    memristor_instance.x = 0
    dx = -0.5
    updated_x = memristor_instance.update_x(dt, dx)
    expected_x = max(memristor_instance.x_off, 0 + dt * dx)
    assert updated_x == expected_x

    # Case 3: No change
    memristor_instance.x = 0.5
    dx = 0
    updated_x = memristor_instance.update_x(dt, dx)
    assert updated_x == 0.5


def test_write_array(memristor_instance):
    """
    Test the write_array function for correct resistance values based on input binary codes.
    """
    array = memristor_instance.crossbar()
    word_code_list = ['11001100', '10101010', '11110000', '00001111', 
                      '00110011', '01010101', '10011001', '01100110']
    
    updated_array = memristor_instance.write_array(array, word_code_list)

    for i, code in enumerate(word_code_list):
        for j, char in enumerate(code):
            if char == '0':
                assert updated_array[j][i] == memristor_instance.Roff
            else:
                assert updated_array[j][i] == memristor_instance.Ron

def test_read_array(memristor_instance):
    """
    Test the read_array function to ensure correct summation based on resistance values.
    """
    array = np.array([[100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100],
                      [100, 100, 100, 100, 100, 100, 100, 100]])
    
    code = '11001100'
    expected_voltage = np.zeros((8, 1))
    for i, char in enumerate(code):
        if char == '0':
            expected_voltage[i] = 0.2
        elif char == '1':
            expected_voltage[i] = 0.008

    expected_result = np.sum(expected_voltage / array, axis=0)
    result = memristor_instance.read_array(code, array)
    
    assert np.allclose(result, expected_result)

if __name__ == '__main__':
    pytest.main()
