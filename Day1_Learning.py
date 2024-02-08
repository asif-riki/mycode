from tabulate import tabulate

# Added new line
def person(name, **data):
    table = [["Name", name]]

    for i, j in data.items():
        table.append([i.capitalize(), j])
        

    print(tabulate(table, headers=[i, j],tablefmt="html"))  #tablefmt="fancy_grid"


person('ABC', age=28, city='KOP', mob=98765)