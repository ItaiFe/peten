Pawn Sides -

Player A - "A"
Player B - "B"
Non Player - "O"

If you're side A - you should place your initial lineup in the first two rows (0,1)
If you're side B - you should place your initial lineup in the last two rows (4,5)

-------------------------------------------------------------------------------------------------------

Pawn Types - 

0 - Tile
1 - Rock (winds scissors)
2 - Paper (wins rock)
3 - Scissors (wins paper)
4 - Trap (wins everything)
5 - Flag (loses to everything)

-------------------------------------------------------------------------------------------------------

Messages (Recieve) -

Side - ["side", side]
It's your turn - "turn"
Send me initial lineup - "initialize_board"
You did an illegal move - "bad_move"
Change_weapon for last move - "change_weapon"
You won - "victory"
You lost - "loser"
New board - ["board", [[pawn_id, pawn_type {if its your pawn or "" if not}, pawn_side, pawn_location] * 6] * 7]

-------------------------------------------------------------------------------------------------------

Responses (Send) - 

Ack (only to Side) - ["ack"]
Move - ["move", pawn_id, source_location([x,y]), dest_location([x,y])]
Change Weapon - ["change", weapon]
Initial Lineup - ["initialize", [[pawn_weapon, location] * 7] * 6]