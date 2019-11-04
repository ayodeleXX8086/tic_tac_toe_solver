from flask import Flask,jsonify,request
from tic_tac_solver import solve_tic_tac,construct_board,check_if_board_is_full,check_winner,convert_board_to_string,FailedValidation


app = Flask(__name__)

@app.route("/tic_tac")
def solve_game():
    """
    :param param:  Board string of 9 characters string with +, X, or O
    The computer is represented as O but the player is represented as X
    """
    try:
        param  = request.args.get("board")
        result = solve_tic_tac(param)
        board  = construct_board(result)
        if check_winner(board): # Check if string which is been returned is a winning string
            winner_detail = check_winner(board)
            message = f"The winner is {winner_detail[0]}"
        elif check_if_board_is_full(board): # Check if the board is full
            message = "This was draw nice play"
        else:
            message = f"The player X will take the next move {board}\n board_format: {convert_board_to_string(board)}"
        return jsonify({"message":message}),200
    except FailedValidation as e:
        return jsonify({"message":"This is not a valid board"}),400
    except KeyError as e:
        return jsonify({"message":"The argument board as to be passed as parameter to this service "}),400


if __name__ == "__main__":
    app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
    app.run(debug=True)



