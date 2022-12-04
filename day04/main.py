import re

if __name__ == '__main__':
    with open('input.txt') as input_file:
        input_data = [line.rstrip('\n') for line in input_file]

    contained = 0
    overlap = 0
    for line_index,line in enumerate(input_data):
        start1, end1, start2, end2 = (int(i) for i in re.split(r'[-,]', line))
        # print(f"{start1} {end1} {start2} {end2}")
        #   ..1234..                               ...23...
        #   ...23...                               ..1234..
        if (start1 <= start2 and end1 >= end2) or (start2 <= start1 and end2 >= end1):
            contained += 1
            overlap += 1
        # ..1234...                        .....456.
        # .....456.                        ..1234...
        elif (start1 <= start2 and end1 >= start2) or (start2 <= start1 and end2 >= start1):
            overlap += 1
    print(f"Fully contained: {contained} | Any overlap: {overlap}")
