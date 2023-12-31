__author__ = "Logan Camp, Hannah Ogden, and Joe Gentlin"
__Copyright__ =  "Copyright @2022"


class circuit(object):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2

class andgate(circuit):
    def getCircuitOutput(self):
        if self.in1_ == 1 and self.in2_ == 1:
            return 1
        else:
            return 0

class orgate(circuit):
    def getCircuitOutput(self):
        if self.in1_ == 0 and self.in2_ == 0:
            return 0
        else:
            return 1

class xorgate(circuit):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2
        not_in1 = notgate(self.in1_) 
        self.out_not1_ = not_in1.getCircuitOutput()
        not_in2 = notgate(self.in2_) 
        self.out_not2_ = not_in2.getCircuitOutput()

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.out_not2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(self.in2_, self.out_not1_)
        out_andg1 = andg1.getCircuitOutput()

        org0 = orgate(out_andg1 , out_andg0)
        out_org0 = org0.getCircuitOutput()

        return out_org0

class notgate(circuit):
    def __init__(self, in1):
        self.in1_ = in1

    def getCircuitOutput(self):
        if self.in1_ == 1:
            return 0
        elif self.in1_ == 0:
            return 1

#Hint: you may implement some multi-input logic gates to help you build the circuit,
#for example, below is a 3-input andgate3 boolean algebra: Y=ABC
class andgate3(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(out_andg0, self.in3_)
        out_andg1 = andg1.getCircuitOutput()

        return out_andg1

#2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):
    def __init__(self, in1, in2, sel):
        self.in1_ = in1
        self.in2_ = in2
        self.sel_ = sel
        not_sel_ = notgate(self.sel_) 
        self.out_not_sel_ = not_sel_.getCircuitOutput()
    
    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.out_not_sel_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(self.in2_ , self.sel_)
        out_andg1 = andg1.getCircuitOutput()

        org0 = orgate(out_andg1 , out_andg0)
        out_org0 = org0.getCircuitOutput()

        return out_org0

#4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):
    def __init__(self, in1, in2, in3, in4, sel2, sel1):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.sel1_ = sel1
        self.sel2_ = sel2
        not_sel1_ = notgate(self.sel1_) 
        self.out_not_sel1_ = not_sel1_.getCircuitOutput()
        not_sel2_ = notgate(self.sel2_) 
        self.out_not_sel2_ = not_sel2_.getCircuitOutput()

    def getCircuitOutput(self):
        mux1 = mux_2to1(self.in1_ , self.in2_ , self.sel1_)
        out_mux1 = mux1.getCircuitOutput()
    
        mux2 = mux_2to1(self.in3_ , self.in4_ , self.sel1_)
        out_mux2 = mux2.getCircuitOutput()

        mux3 = mux_2to1(out_mux1, out_mux2 , self.sel2_)
        out_mux3 = mux3.getCircuitOutput()

        return out_mux3

#fulladder implemented with logic gates
class fulladder(circuit):
    def __init__(self, in1, in2, cin):
        self.in1_ = in1
        self.in2_ = in2
        self.cin_ = cin
    
    def getCircuitOutput(self):
        xor0 = xorgate(self.in1_, self.in2_)
        out_xor0 = xor0.getCircuitOutput()

        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(out_xor0 , self.cin_)
        out_andg1 = andg1.getCircuitOutput()

        xor1 = xorgate(out_xor0 , self.cin_)
        sum_ = xor1.getCircuitOutput()

        org0 = orgate(out_andg0 , out_andg1)
        cout_ = org0.getCircuitOutput()
        return(sum_ , cout_)


    '''
    Implement a 1-bit ALU by using the above circuits, e.g.,  mux_2to1, fulladder and mux_4to1, etc.
    '''



class ALU_1bit(object):
    def __init__(self, Ainvert, Binvert, op1, op0, bitA, bitB, cin=None, less=0):
        self.Avert = Ainvert
        self.Bvert = Binvert
        self.op1 = op1
        self.op0 = op0
        self.bitA = bitA
        self.bitB = bitB
        self.cin = cin
        self.less = less
        self.notA = notgate(self.bitA).getCircuitOutput()
        self.notB = notgate(self.bitB).getCircuitOutput()

        if self.cin == None and Ainvert == 0 and Binvert == 1 and op1 == 1 and op0 == 0:
            self.cin = 1
        elif self.cin == None:
            self.cin = 0
            
    def getCircuitOutput(self):
        if self.Avert == 0 and self.Bvert == 0 and self.op1 == 0 and self.op0 == 0:
            ALUand = andgate(self.bitA, self.bitB)
            result = ALUand.getCircuitOutput()
        elif self.Avert == 0 and self.Bvert == 0 and self.op1 == 0 and self.op0 == 1:
            ALUor = orgate(self.bitA, self.bitB)
            result = ALUor.getCircuitOutput()
        elif self.Avert == 0 and self.Bvert == 0 and self.op1 == 1 and self.op0 == 0:
            ALUadd = fulladder(self.bitA, self.bitB, self.cin)
            result = ALUadd.getCircuitOutput()
        elif self.Avert == 0 and self.Bvert == 1 and self.op1 == 1 and self.op0 == 0:
            ALUsub = fulladder(self.bitA, notgate(self.bitB), self.cin)
            result = ALUsub.getCircuitOutput()
        elif self.Avert == 0 and self.Bvert == 1 and self.op1 == 1 and self.op0 == 1:
            result = self.less
        elif self.Avert == 1 and self.Bvert == 1 and self.op1 == 0 and self.op0 == 0:
            result = orgate(self.notA, self.notB)
        return result



class aluControl(circuit):
    def __init__(self, aluOp1, aluOp0, f5, f4, f3, f2, f1, f0):
        self.aluOp0_ = aluOp0
        self.aluOp1_ = aluOp1
        self.f5_ = f5
        self.f4_ = f4
        self.f3_ = f3
        self.f2_ = f2
        self.f1_ = f1
        self.f0_ = f0
    
    def getCircuitOutput(self):
        org0 = orgate(self.f0_ , self.f3_)
        out_org0_ = org0.getCircuitOutput()

        andg0 = andgate(self.aluOp1_ , self.f1_)
        out_andg0_ = andg0.getCircuitOutput()

        andg1 = andgate(self.aluOp1_ , out_org0_)
        op0 = andg1.getCircuitOutput()

        not_aluOp0 = notgate(self.aluOp0_)
        out_notAOp0 = not_aluOp0.getCircuitOutput()

        andg2 = andgate(self.aluOp0_ , out_notAOp0)
        op3 = andg2.getCircuitOutput()

        org1 = orgate(self.aluOp0_ , out_andg0_)
        op2 = org1.getCircuitOutput()

        not_aluOp1 = notgate(self.aluOp1_)
        out_notAOp1_ = not_aluOp1.getCircuitOutput()

        not_f2 = notgate(self.f2_)
        out_notF2_ = not_f2.getCircuitOutput()

        org2 = orgate(out_notAOp1_ , out_notF2_)
        op1 = org2.getCircuitOutput()

        return(op3 , op2 , op1 , op0)

        
    '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0.
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''



class ALU_32bit(object):
    def __init__(self, Ainvert , Binvert , op1 , op0, Aval, Bval, less=0):
        self.Avert = Ainvert
        self.Bvert = Binvert
        self.op1 = op1
        self.op0 = op0
        self.Aval = Aval
        self.Bval = Bval
        self.less = less
        self.cin = None
        self.result = []

        reg_initial_value = [0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 0, 0,   0, 0, 1, 0]
        self.temp_reg_file = registerFile(reg_initial_value)

    def getCircuitOutput(self):
        for i in reversed(range(1, 32)):
            bit_result = ALU_1bit(self.Avert, self.Bvert, self.op1, self.op0, self.Aval[i], self.Bval[i], self.cin, self.less).getCircuitOutput()
            if type(bit_result) is tuple:
                self.result.append(bit_result[0])
                self.cin = bit_result[1]
            else:
                self.result.append(bit_result)

        bit_result = ALU_1bit(self.Avert, self.Bvert, self.op1, self.op0, self.Aval[0], self.Bval[0], self.cin, self.less).getCircuitOutput()
        if type(bit_result) is tuple:
            self.result.append(bit_result[0])
            self.cin = bit_result[1]
        else:
            self.result.append(bit_result)

        self.less = self.result[-1]
        self.less = ALU_32bit(0,0,0,0, self.less, self.temp_reg_file.getRegValue("zero"))

        self.result.reverse()
        return self.result


    '''
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with lenth 32, e.g.:
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0 of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31th one should be the carryIn the next 1 bit ALU, you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31th 1-bit ALU and make it as the less input of the 0th 1bit ALU.
    '''



class registerFile(circuit):
    def __init__(self, reg_initial_value) :
        self.zero_register = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.regValues = []
        #makes a 2d array of all registers
        for i in range(32):
            self.regValues.append(reg_initial_value)

    def setRegValue(self, o_regDecoder, valueToSet):
        reg_num = int(''.join(str(n) for n in o_regDecoder), 2)
        self.regValues[reg_num] = valueToSet

    def getRegValue(self, o_regDecoder):
        if o_regDecoder == "zero":
            register = self.zero_register
        else:
            #converts the decoder output to decimal
            reg_num = int(''.join(str(n) for n in o_regDecoder), 2)
            register = self.regValues[reg_num]
        return register

    def getAllRegValues(self):
        return self.regValues



class decoderReg(circuit):
    def __init__(self, InstrRegFiled):
        self.reg = InstrRegFiled

    def getCircuitOutput(self):
        register = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, *self.reg]
        return register



class mainCtrol(circuit):
    def __init__(self, instruction):
        self.instruction = instruction

    def getCircuitOutput(self):
        if self.instruction == [0, 0, 0, 0, 0, 0]:
            alu_op = [1,0]
        elif ((self.instruction)  == [1, 0, 0, 0, 1, 1]) | ((self.instruction)  == [1, 0, 1, 0, 1, 1] ):
            alu_op = [0,0]
        elif ((self.instruction)  == [0, 0, 0, 1, 0, 0]):
            alu_op = [0,1]
        else:
            print("ERROR OP CODE")

        return alu_op



class simpleMIPS(circuit):
    def __init__(self, registers):
        self.registers = registers
        self.aluOperationCode = []

    def getCircuitOutput(self, instruction):
        rs = decoderReg(instruction[6:11]).getCircuitOutput()
        rt = decoderReg(instruction[11:16]).getCircuitOutput()
        rd = decoderReg(instruction[16:21]).getCircuitOutput()

        alu_op = mainCtrol(instruction[0:6]).getCircuitOutput()
        alucontrolCode = alu_op + instruction[26:32]
        self.aluOperationCode = aluControl(*alucontrolCode)

        A = self.registers.getRegValue(rs)
        B = self.registers.getRegValue(rt)
        result = ALU_32bit(*self.aluOperationCode.getCircuitOutput(), A, B).getCircuitOutput()
        self.registers.setRegValue(rd, result)
