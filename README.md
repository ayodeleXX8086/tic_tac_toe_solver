                    **Tic Tac Toe Solver**
Use pip install -r requirements.txt to install all the dependencies

Run the application using this command python tic_tac_server.py

It will start the server http://localhost:5000/tic_tac?board=+++++++++
 then you could start playing, A tic tac toe is a 3 by 3 board which on a one dimension it represented with a list of 9 length.

Computer is represented as O
Player should be represented as X

board_str:+++++++++  **-->** is a string with length 9 with characters such as +,X,O
Move the character to 1 dimension location, as it will be on a 3 by 3 matrix.

 
 Response type
 
`{
message: "The player X will take the next move [[' ', ' ', ' '], [' ', ' ', ' '], [' ', 'O', ' ']] board_format: +++++++O+"
}`
