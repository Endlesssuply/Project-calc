from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math

import operator

from MainWindow import Ui_MainWindow

# Константы
READY = 0
INPUT = 1


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Задаем числа
        for n in range(0, 10):
            getattr(self, 'pushButton_n%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        # Задаем операции
        self.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
        self.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv))
        self.pushButton_ste.pressed.connect(lambda: self.operation(operator.pow))
        
        self.pushButton_root1.pressed.connect(self.operation_root1)
        self.pushButton_root2.pressed.connect(self.operation_root2)
        self.pushButton_pow1.pressed.connect(self.operation_pow1)
        self.pushButton_pow2.pressed.connect(self.operation_pow2)
        self.pushButton_inv.pressed.connect(self.operation_inv)
        self.pushButton_pi.pressed.connect(self.operation_pi)
        self.pushButton_pc.pressed.connect(self.operation_pc)
        self.pushButton_fact.pressed.connect(self.operation_fact)        
        self.pushButton_exp.pressed.connect(self.operation_exp)
        self.pushButton_log.pressed.connect(self.operation_log)        
        self.pushButton_eq.pressed.connect(self.equals)
        
        # Задаем действия
        self.actionReset.triggered.connect(self.reset)
        self.pushButton_ac.pressed.connect(self.reset)

        self.pushButton_m.pressed.connect(self.memory_store)
        self.pushButton_mr.pressed.connect(self.memory_recall)

        self.memory = 0
        self.reset()

        self.show()

    def display(self):
        self.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def memory_store(self):
        self.memory = self.lcdNumber.value()

    def memory_recall(self):
        self.state = INPUT
        self.stack[-1] = self.memory
        self.display()

    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()

    def operation(self, op):
        if self.current_op:  # Завершить текущую операцию
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()
    
    def operation_inv(self):
        self.state = INPUT
        self.stack[-1] *= -1
        self.display()
    
    def operation_root1(self):
        self.state = INPUT
        self.stack[-1] **= 0.5
        self.display()    

    def operation_root2(self):
        self.state = INPUT
        self.stack[-1] **= (1/3)
        self.display()
        
    def operation_pow1(self):
        self.state = INPUT
        self.stack[-1] **= 2
        self.display()    

    def operation_pow2(self):
        self.state = INPUT
        self.stack[-1] **= 3
        self.display()
        
    def operation_pi(self):
        self.state = INPUT
        self.stack[-1] = 3.14159265359
        self.display()
    
    def operation_exp(self):
        self.state = INPUT
        i = 1
        e = 2.71828182846
        print(self.stack[-1])
        while i != self.stack[-1]:
            i += 1
            e *= 2.71828182846
        self.stack[-1] = e
        self.display()
    
    def operation_fact(self):
        self.state = INPUT
        self.stack[-1] = math.factorial(self.stack[-1])
        self.display()
        
    def operation_log(self):
        self.state = INPUT
        self.stack[-1] = math.log(self.stack[-1])
        self.display()
        
    def equals(self):
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            self.stack = [self.current_op(*self.stack)]
            self.current_op = None
            self.state = READY
            self.display()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Calculator")

    window = MainWindow()
    app.exec_()
