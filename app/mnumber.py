from fractions import Fraction

class MNumber:
    def __init__(self,number,coeficient):
        self.number=Fraction(number,1)
        self.coeficient=Fraction(coeficient,1)

    def __add__(self,mnumber):
        number=self.number+mnumber.number
        coeficient=self.coeficient+mnumber.coeficient
        return MNumber(number,coeficient)
    
    def __mul__(self,mnumber):
        if isinstance(mnumber,Fraction):
            number=self.number*mnumber
            coeficient=self.coeficient*mnumber
            return MNumber(number,coeficient)
        if isinstance(mnumber,int):
            number=self.number*mnumber
            coeficient=self.coeficient*mnumber
            return MNumber(number,coeficient)
        number=self.number*mnumber.number
        coeficient=self.coeficient*mnumber.coeficient
        return MNumber(number,coeficient)
    
    def __lt__(self,mnumber):
        if isinstance(mnumber,int):
            if self.coeficient == 0:
                return self.number<mnumber
            return self.coeficient<mnumber
        if self.coeficient == mnumber.coeficient:
            return self.number<mnumber.number
        return self.coeficient<mnumber.coeficient
    
    def __str__(self):
        if self.number == 0:
            return '{}M'.format(self.coeficient)
        if self.coeficient == 0:
            return '{}'.format(self.number)
        if self.coeficient<0:
            return '{}{}M'.format(self.number,self.coeficient)
        return '{}+{}M'.format(self.number,self.coeficient)