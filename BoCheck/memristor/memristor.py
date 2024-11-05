import numpy as np


class memristor:
    """
    A class to simulate a memristor with customizable parameters and a crossbar array structure.
    """

    def __init__(self):
        """
        Initializes the memristor with default parameter values.
        """
        self.alpha_pos = 1
        self.alpha_neg = 3
        self.v_pos = 0.5
        self.v_neg = -0.5
        self.Ron = 100
        self.Roff = 2500
        self.Kpos = 80
        self.Kneg = -120
        self.x_off = 0
        self.x_on = 1
        self.r = 100  # Default resistance value
        self.x = 1    # Default memristor state value

    def dx(self, v): # dw(t)/dt
        """
        Calculates the rate of change of the memristor state based on the input voltage.

        Parameters:
        v (float): Input voltage applied to the memristor.

        Returns:
        dx (float): Rate of change of the state variable.
        """
        if v > self.v_pos:
            dx = self.Kpos * (v / self.v_pos - 1) ** self.alpha_pos
        elif self.v_neg <= v <= self.v_pos:
            dx = 0
        else:
            dx = self.Kneg * (v / self.v_neg - 1) ** self.alpha_neg
        return dx

    def R(self):
        """
        Calculates the current resistance of the memristor based on its state variable.

        Returns:
        R (float): Current resistance of the memristor.
        """
        R = self.Ron + (self.Roff - self.Ron) * (1 - self.x)
        return R

    def update_x(self, dt, dx):
        """
        Updates the state variable of the memristor over a given time step.

        Parameters:
        dt (float): Time step for updating the state.
        dx (float): Rate of change of the state variable.

        Returns:
        x (float): Updated state of the memristor.
        """
        self.x = self.x + dt * dx
        if self.x > self.x_on:
            self.x = self.x_on
        elif self.x < self.x_off:
            self.x = self.x_off
        x = self.x
        return x

    def crossbar(self):
        """
        Creates an 8x50 crossbar array to represent multiple memristors in a matrix.

        Returns:
        array (np.ndarray): Initialized crossbar array with zeros.
        """
        array = np.zeros([8, 50])
        return array

    def write_array(self, array, word_code_list):
        """
        Writes a list of word codes into the memristor crossbar array, where '1' indicates
        a low resistance state (100 ohms) and '0' indicates a high resistance state (2500 ohms).

        Parameters:
        array (np.ndarray): The crossbar array to be modified.
        word_code_list (list): List of binary codes for the memristors in each row of the array.

        Returns:
        array (np.ndarray): Updated crossbar array with new resistance values.
        """
        array = np.zeros([8, 50])
        column = 0
        for i in range(len(word_code_list)):
            for j in range(8):
                if word_code_list[i][j] == '0':
                    array[j][i] = 2500
                else:
                    array[j][i] = 100
        array[array == 0] = 2500
        return array  

    def read_array(self, code, array):
        """
        Reads values from the crossbar array based on an input code and returns the summed result.

        Parameters:
        code (str): Binary code to specify which elements of the array to read.
        array (np.ndarray): Crossbar array containing resistance values.

        Returns:
        result (float): Summed result of voltage divided by array resistance values.
        """
        voltage = np.zeros([8, 1])
        for i in range(len(code)):
            if code[i] == '0':
                voltage[i] = 0.2
            elif code[i] == '1':
                voltage[i] = 0.008
        result = np.sum(voltage / array, axis=0)
        return result

    # def position_recognization(self,code_list,words,words_code):
    #     if len(code_list) == 1:
    #         for code in code_list:
    #             crossbar_array = self.crossbar()
    #             crossbar_array = self.write_array(crossbar_array,words_code)
    #             result = self.read_array(code,crossbar_array)
    #             print(result)
    #             print('基字：', words[int(np.argwhere(result==0.00064))])
    #     elif len(code_list) == 2:
    #         for code in code_list:

    # def apply_voltage(self, voltage, array):
    #     #voltage是输入的电压序列，array是要进行读取的交叉阵列


class Flux_Controlled_Memristor:
    """
    A class to simulate a memristor with customizable parameters and a crossbar array structure.
    """
    def __init__(self):
        """
        Initializes the memristor with default parameter values.
        """
        self.phi_off = 0
        self.phi_on = 1
        self.phi_pos = 0.5
        self.phi_neg = -0.5
        self.r = 100  # Default resistance value
        self.phi = 0  # Default memristor state value
        #self.alpha = 1 / 10000
        #self.beta = 1 / (10*10000* 2*10e-7 *10000) / 2
        #self.gamma = 1 / (100 * 10000**2 * (2*10e-7)**2 * 10000**2)
        #self.alpha = 1
        #self.beta = 0.5
        #self.gamma = 0.3333
        self.alpha = 100
        self.beta = 0.5
        self.gamma = 2631.14

    def d_phi(self, v): # dw(t)/dt
        """
        Calculates the rate of change of the memristor state based on the input voltage.

        Parameters:
        v (float): Input voltage applied to the memristor.

        Returns:
        d_phi (float): Rate of change of the state variable.
        """
        d_phi = v
        return d_phi

    def R(self):
        """
        Calculates the current resistance of the memristor based on its state variable.

        Returns:
        R (float): Current resistance of the memristor.
        """
        R = self.alpha + 2*self.beta*self.phi + 3*self.gamma*self.phi**2
        return R

    def update_phi(self, dt, d_phi):
        """
        Updates the state variable of the memristor over a given time step.

        Parameters:
        dt (float): Time step for updating the state.
        d_phi (float): Rate of change of the state variable.

        Returns:
        phi (float): Updated state of the memristor.
        """
        if d_phi > self.phi_pos or d_phi < self.phi_neg:
            self.phi = self.phi + dt * d_phi
        else:
            self.phi = self.phi
        #self.phi = self.phi + dt * d_phi
        #if self.phi > self.phi_on:
        #    self.phi = self.phi_on
        #elif self.phi < self.phi_off:
        #    self.phi = self.phi_off
        phi = self.phi
        return phi

    def crossbar(self):
        """
        Creates an 8x50 crossbar array to represent multiple memristors in a matrix.

        Returns:
        array (np.ndarray): Initialized crossbar array with zeros.
        """
        array = np.zeros([8, 50])
        return array

    def write_array(self, array, word_code_list):
        """
        Writes a list of word codes into the memristor crossbar array, where '1' indicates
        a low resistance state (100 ohms) and '0' indicates a high resistance state (2500 ohms).

        Parameters:
        array (np.ndarray): The crossbar array to be modified.
        word_code_list (list): List of binary codes for the memristors in each row of the array.

        Returns:
        array (np.ndarray): Updated crossbar array with new resistance values.
        """
        array = np.zeros([8, 50])
        column = 0
        for i in range(len(word_code_list)):
            for j in range(8):
                if word_code_list[i][j] == '0':
                    array[j][i] = 2500
                else:
                    array[j][i] = 100
        array[array == 0] = 2500
        return array  

    def read_array(self, code, array):
        """
        Reads values from the crossbar array based on an input code and returns the summed result.

        Parameters:
        code (str): Binary code to specify which elements of the array to read.
        array (np.ndarray): Crossbar array containing resistance values.

        Returns:
        result (float): Summed result of voltage divided by array resistance values.
        """
        voltage = np.zeros([8, 1])
        for i in range(len(code)):
            if code[i] == '0':
                voltage[i] = 0.2
            elif code[i] == '1':
                voltage[i] = 0.008
        result = np.sum(voltage / array, axis=0)
        return result
