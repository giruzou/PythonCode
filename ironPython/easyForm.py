#!/usr/bin/ipy
import clr

clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import Application, Form

class IForm(Form):

    def __init__(self):
        self.Text = 'Simple'
        self.Width = 250
        self.Height = 200
        self.CenterToScreen()

def main():
    Application.Run(IForm())

if __name__ == '__main__':
    main()
