import protogdata, battleactions, battleloop

endturn = False
attackSelected = False
choice = 0
attack = 0

while endturn == False:

    choice = battleloop.actionChoice()

    if choice == 1:
        attack = battleloop.attackChoice()
        if attack != 0:
            attackSelected = True
            endturn = True
    if choice == 4:
        endturn = True


