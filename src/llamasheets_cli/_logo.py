from rich.console import Console
from rich_gradient.text import Text

LOGO = """
     ==                                                         
     ====                                                       
   ======                                                       
     ===++                                                      
     +++++                                                      
     +++++++*++                                                 
     +++++++++++=======-                                        
     +++++++++======-----                                       
      +++++=======------                                        
       ++======---------                                        
        =====-----------                                        
         ==--     ------                                        
         ---        - ==                                        
         - -        =  =                                        
        ----      ==  ==                                      
"""

WRITING = """
░█░░░█░░░█▀█░█▄█░█▀█░█▀▀░█░█░█▀▀░█▀▀░▀█▀░█▀▀
░█░░░█░░░█▀█░█░█░█▀█░▀▀█░█▀█░█▀▀░█▀▀░░█░░▀▀█
░▀▀▀░▀▀▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░░▀░░▀▀▀  
"""


def print_logo() -> None:
    cs = Console()
    print("\n")
    cs.print(
        Text(LOGO, colors=["#4B72FE", "#FF8DF2", "#FF8705"]),
        justify="left",
    )
    print("\n")
    cs.print(
        Text(WRITING, colors=["#4B72FE", "#FF8DF2", "#FF8705"]),
        justify="left",
    )
    print("\n")
