'''
python code to transform pgn file into a csv format
'''
import sys
import chess.pgn
from itertools import islice
import pandas as pd

VALID_FIELDS = [
    'Event',
    'Site',
    'White',
    'Black',
    'WhiteElo',
    'BlackElo',
    'WhiteRd',
    'BlackRd',
    'TimeControl',
    'Date',
    'ECO',
    'PlyCount',
    'Result',
    'Movements'
]

def read_single_game(games):
    game = []
    found_game = False
    while True:
        line = games.readline()
        if not line:
            break
        game.append(line)
        if line[:2] == '1.':
            found_game = True
            break
    if found_game == True:
        return game
    
    return None

        

def record_field(key, value, field_dict):
    if key in VALID_FIELDS:
        field_dict[key] = value

def main(file_path, file_name):
    print("converting PGN to CSV")
    
    # create an empty pandas DataFrame
    rows = []

    # open file
    with open(file_path + '/' + file_name, 'r') as games:
        while True:
            # each 20 times represent a game
            game = read_single_game(games)
            # create a game dictionary to record the fields
            game_dict = {}
            # return if there are no more games to parse
            if not game:
                break
            # return if its EOF
            if len(game) == 0 or len(game) == 1:
                break
            # loop over the individual descriptors of the game
            for field in game:
                # print("field:", field)
                # strip the field
                field = field.strip()
                # check if field is empty
                if (field == None or field == ''):
                    continue
                # check if field is wrapped with []
                if (field[0] == '[' and field[-1] == ']'):
                    # strip it
                    field = field[1:-1]
                    key, value = field.split(' ', 1)
                    # string the quotations from the value
                    value = value[1:-1]
                    # record the field to the game dictionary
                    record_field(key, value, game_dict)
                if field[:2] == '1.':
                    record_field('Movements', field, game_dict)

            # create a pandas series from the game dictionary
            series = pd.Series(game_dict)
            rows.append(series)
        # close the file once processing is done
        games.close()
    
    # create a dataframe from the rows
    dataframe = pd.DataFrame(rows)
    print(dataframe)

    file_name_without_ext = file_name.split('.')[0]

    # export the dataframe as a 
    dataframe.to_csv(file_path + '/' + file_name_without_ext + '.csv', index=False)
           
if __name__ == "__main__":
    # first argument should be the path of the pgn file to process
    file_path_from_root = sys.argv[1]
    file_name = sys.argv[2]

    main(file_path_from_root, file_name)
