import time

from rich.live import Live
from rich.table import Table

'''
A script to veiw data
'''

# Test sample
card_data = [{'name': 'Crimson Butterfly, Brigitte', 'power': '10000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': "[AUTO](VC): When this unit's drive check reveals a grade 3 «\nRoyal Paladin\n», this unit gets [Power]+5000 until end of that battle."}, {'name': 'Knight of Conviction, Bors', 'power': '10000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '[AUTO](VC/RC):[Counter Blast (1)] When this unit attacks, you may pay the cost. If you do, this unit gets [Power]+3000 until end of that battle.'}, {'name': 'Solitary Knight, Gancelot', 'power': '9000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '[ACT](VC):[Counter Blast (2)] If you have a card named "\nBlaster Blade\n" in your soul, this unit gets [Power]+5000/[Critical]+1 until end of turn.\n[ACT](Hand):[Reveal this card to your opponent, and put it on top of your deck] Search your deck for up to one card named "Blaster Blade", reveal it to your opponent, put it into your hand, and shuffle your deck.'}, {'name': 'Knight of Silence, Gallatin', 'power': '10000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}, {'name': 'Blaster Blade', 'power': '9000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': "[AUTO]:[Counter Blast (2)] When this unit is\nplaced\non (VC), you may pay the cost. If you do, choose one of your opponent's rear-guards, and retire it.\n[AUTO]:[Counter Blast (2)] When this unit is placed on (RC), if you have a «\nRoyal Paladin\n» vanguard, you may pay the cost. If you do, choose one of your opponent's grade 2 or greater rear-guards, and retire it."}, {'name': 'Knight of the Harp, Tristan', 'power': '8000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': "[AUTO](VC): When this unit's drive check reveals a grade 3 «\nRoyal Paladin\n», this unit gets [Power]+5000 until end of that battle."}, {'name': 'Covenant Knight, Randolf', 'power': '8000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': "[AUTO](VC/RC):When this unit attacks, if the number of cards in your hand is greater than your opponent's, this unit gets [Power]+3000 until end of that battle."}, {'name': 'Little Sage, Marron', 'power': '8000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}, {'name': 'Wingal', 'power': '6000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '[AUTO](RC):When this unit\nboosts\na card named "\nBlaster Blade\n", the boosted unit gets [Power]+4000 until end of that battle.'}, {'name': 'Starlight Unicorn', 'power': '6000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '[AUTO]:When this unit is placed on (RC), choose another of your «\nRoyal Paladin\n», and that unit gets [Power]+2000 until end of turn.'}, {'name': 'Knight of Rose, Morgana', 'power': '6000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '[AUTO](VC/RC):[Choose a card from your hand, and discard it] When this unit attacks, you may pay the cost. If you do, this unit gets [Power]+4000 until end of turn.'}, {'name': 'Stardust Trumpeter', 'power': '6000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}, {'name': 'Bringer of Good Luck, Epona', 'power': '5000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}, {'name': 'Yggdrasil Maiden, Elaine', 'power': '5000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': '(You may only have up to four cards with "HEAL" in a\ndeck\n.)'}, {'name': 'Weapons Dealer, Govannon', 'power': '5000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}, {'name': 'Flogal', 'power': '5000', 'critical': '1', 'clan': 'Royal Paladin', 'effect': None}]


def generate_table(card_data):
    """
    Generate a table base on the list-dict data

    Parameter:
    card_data (list-dict)

    Returns:
    A table by rich
    """

    # Get the first element keys
    headers = list(card_data[0].keys())

    # Initialize table
    table = Table(title="[bold cyan]Live CSV Data Feed[/bold cyan]")
    for header in headers:
        table.add_column(header, style="magenta")

    # Build Table
    with Live(table, refresh_per_second=4) as _:
        for row in card_data:
            if row:
                table.add_row(* row.values())

                # Adjust sleep to increase/decrease build time
                time.sleep(0.2)

def main():
    """Example execution"""

    generate_table(card_data)

if __name__ == "__main__":
    main()
